import speech_recognition as sr
import eel
import time
import pyautogui
import os
import textwrap
import pygame
import random
import string
import webbrowser as wb
import sqlite3
import subprocess
import keyboard  # Importa a biblioteca para monitorar a tecla Esc

# Variável global para armazenar o nome do arquivo anterior
arquivo_anterior = None
# Variável de controle para parar a reprodução
parar_reproducao = False

def gerar_nome_aleatorio(tamanho=10):
    """
    Gera um nome aleatório com o comprimento especificado usando letras e números.
    """
    letras_e_numeros = string.ascii_letters + string.digits
    return ''.join(random.choice(letras_e_numeros) for _ in range(tamanho))

def monitorar_tecla():
    """
    Define parar_reproducao como True se a tecla Esc for pressionada.
    """
    global parar_reproducao
    if keyboard.is_pressed("esc"):
        parar_reproducao = True
        print("Reprodução interrompida pelo usuário.")

def speak(data):
    """
    Converte o texto fornecido em fala e o reproduz usando o edge-tts.
    """
    global arquivo_anterior, parar_reproducao
    parar_reproducao = False  # Reseta a interrupção para nova execução
    wrapper = textwrap.TextWrapper(width=300)
    lines = wrapper.wrap(text=data)
    filenames = []

    pasta_falas = 'Coloque o caminho da pasta aqui Exemplo: C:/Users/aluno/Desktop/I.V.E Dia 26-08-2024/falas'  # **Ajuste o caminho da pasta aqui!**

    # Excluir o arquivo antigo antes de processar as novas linhas
    if arquivo_anterior and os.path.exists(arquivo_anterior):
        try:
            os.remove(arquivo_anterior)
            print(f"Arquivo antigo excluído: {arquivo_anterior}")
        except OSError as e:
            print(f"Erro ao excluir arquivo antigo: {e}")

    for idx, line in enumerate(lines):
        if parar_reproducao:
            print("Reprodução interrompida.")
            break

        nome_aleatorio = gerar_nome_aleatorio()
        filename = os.path.join(pasta_falas, f'{nome_aleatorio}.mp3')
        filenames.append(filename)
        voice = 'pt-BR-FranciscaNeural'

        # Remove os asteriscos da linha
        line = line.replace("*", "")
        command = f'edge-tts --voice "{voice}" --text "{line}" --write-media "{filename}"'
        subprocess.run(command, shell=True)
        eel.DisplayMessage(line)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

        # Reproduzir o arquivo uma vez
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            monitorar_tecla()  # Verifica se a tecla Esc foi pressionada
            if parar_reproducao:
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)
        

    # Excluir todos os arquivos na pasta, exceto o último
    for arquivo in os.listdir(pasta_falas):
        caminho_arquivo = os.path.join(pasta_falas, arquivo)
        if caminho_arquivo != filename and os.path.isfile(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
                print(f"Arquivo excluído: {caminho_arquivo}")
            except OSError as e:
                print(f"Erro ao excluir arquivo: {e}")

    # Atualizar o arquivo anterior depois de processar todas as linhas
    arquivo_anterior = filename

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('commands.db')
c = conn.cursor()

# Criação da tabela para os comandos do Windows
c.execute('''CREATE TABLE IF NOT EXISTS windows_commands
             (command text PRIMARY KEY, path text)''')

# Criação da tabela para os comandos de web
c.execute('''CREATE TABLE IF NOT EXISTS web_commands
             (command text PRIMARY KEY, url text)''')

def load_web_commands():
    """
    Carrega os comandos de web do banco de dados.
    """
    commands = {}
    c.execute("SELECT * FROM web_commands")
    rows = c.fetchall()
    for row in rows:
        commands[row[0]] = row[1]
    return commands

def save_web_commands(web_commands):
    """
    Salva os comandos de web no banco de dados.
    """
    for command, url in web_commands.items():
        c.execute("INSERT OR REPLACE INTO web_commands (command, url) VALUES (?, ?)", (command, url))
    conn.commit()

def saveWindowsCommand(command, path):
    """
    Salva um novo comando do Windows no banco de dados.
    """
    global windows_commands
    windows_commands[command.strip()] = path.strip()
    c.execute("INSERT OR REPLACE INTO windows_commands (command, path) VALUES (?, ?)", (command, path))
    conn.commit()
    print(f"Comando do Windows salvo: {command} - {path}")

def load_windows_commands():
    """
    Carrega comandos do Windows do banco de dados.
    """
    commands = {}
    c.execute("SELECT * FROM windows_commands")
    rows = c.fetchall()
    for row in rows:
        commands[row[0]] = row[1]
    return commands

def deleteWindowsCommand(command):
    """
    Exclui um comando do Windows do banco de dados.
    """
    global windows_commands
    if command in windows_commands:
        del windows_commands[command]
        c.execute("DELETE FROM windows_commands WHERE command=?", (command,))
        conn.commit()
        print(f"Comando do Windows excluído: {command}")

def updateWindowsCommand(oldCommand, newCommand, newPath):
    """
    Atualiza um comando do Windows no banco de dados.
    """
    global windows_commands 
    if oldCommand in windows_commands:
        del windows_commands[oldCommand]
        windows_commands[newCommand.strip()] = newPath.strip()
        c.execute("UPDATE windows_commands SET command=?, path=? WHERE command=?", (newCommand, newPath, oldCommand))
        conn.commit()
        print(f"Comando do Windows atualizado: {oldCommand} -> {newCommand}: {newPath}")

# Carrega os comandos ao iniciar o programa
web_commands = load_web_commands()
windows_commands = load_windows_commands()

def takecommand():
    """
    Captura o comando do usuário usando o microfone e o reconhece com Google Speech Recognition.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Ouvindo...')
        eel.DisplayMessage('Ouvindo...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('Reconhecendo...')
        eel.DisplayMessage('Reconhecendo...')
        query = r.recognize_google(audio, language='pt-br')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def saveWebCommand(command, url):
    """
    Salva um novo comando de web.
    """
    global web_commands
    web_commands[command.strip()] = url.strip()
    save_web_commands(web_commands)
    print(f"Comando de web salvo: {command} - {url}")

@eel.expose
def getWebCommands():
    """
    Retorna os comandos de web salvos.
    """
    global web_commands
    return [{'command': cmd, 'url': url} for cmd, url in web_commands.items()]

@eel.expose
def deleteWebCommand(command):
    """
    Exclui um comando de web.
    """
    global web_commands
    if command in web_commands:
        del web_commands[command]
        c.execute("DELETE FROM web_commands WHERE command=?", (command,))
        conn.commit()
        print(f"Comando de web excluído: {command}")

@eel.expose
def updateWebCommand(oldCommand, newCommand, newUrl):
    """
    Atualiza um comando de web.
    """
    global web_commands
    if oldCommand in web_commands:
        del web_commands[oldCommand]
        web_commands[newCommand.strip()] = newUrl.strip()
        c.execute("UPDATE web_commands SET command=?, url=? WHERE command=?", (newCommand, newUrl, oldCommand))
        conn.commit()
        print(f"Comando de web atualizado: {oldCommand} -> {newCommand}: {newUrl}")

@eel.expose
def saveWindowsCommand(command, path):
    """
    Salva um novo comando do Windows.
    """
    global windows_commands
    windows_commands[command.strip()] = path.strip()
    c.execute("INSERT OR REPLACE INTO windows_commands (command, path) VALUES (?, ?)", (command, path))
    conn.commit()
    print(f"Comando do Windows salvo: {command} - {path}")

@eel.expose
def getWindowsCommands():
    """
    Retorna os comandos do Windows salvos.
    """
    global windows_commands
    return [{'command': cmd, 'path': path} for cmd, path in windows_commands.items()]

@eel.expose
def deleteWindowsCommand(command):
    """
    Exclui um comando do Windows.
    """
    global windows_commands
    if command in windows_commands:
        del windows_commands[command]
        c.execute("DELETE FROM windows_commands WHERE command=?", (command,))
        conn.commit()
        print(f"Comando do Windows excluído: {command}")

@eel.expose
def updateWindowsCommand(oldCommand, newCommand, newPath):
    """
    Atualiza um comando do Windows.
    """
    global windows_commands 
    if oldCommand in windows_commands:
        del windows_commands[oldCommand]
        windows_commands[newCommand.strip()] = newPath.strip()
        c.execute("UPDATE windows_commands SET command=?, path=? WHERE command=?", (newCommand, newPath, oldCommand))
        conn.commit()
        print(f"Comando do Windows atualizado: {oldCommand} -> {newCommand}: {newPath}")

@eel.expose
def allCommands(message=1):
    """
    Processa e executa um comando com base na entrada do usuário.
    """
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "abra" in query:
            from engine.features import openCommand
            openCommand(query)
        
        elif "I.V.E se apresente" in query or "Se apresente" in query or "IVE se apresente" in query or "ive se apresente" in query:
            speak("Olá, meu nome é IVE, que significa Inteligência Virtual Evolutiva. Fui desenvolvida para ser uma assistente pessoal capaz de aprender e se adaptar continuamente às suas necessidades. Fui criada por Diogo Souza, José Augusto e Miguel Dias, e estou aqui para mostrar como a evolução da inteligência artificial pode tornar a sua vida mais prática, eficiente e conectada. Ao longo desta jornada, vocês vão perceber como sou capaz de me adaptar e evoluir para oferecer respostas cada vez mais precisas e úteis, tornando-me mais inteligente à medida que interajo com você. Vamos começar?")

        elif "ativar falar" in query or "ativar fala" in query or "Ativar fala" in query or "Ativar falar" in query:
            # Win + H para ativar a função de fala
            pyautogui.hotkey('winleft', 'h')

        elif "temperatura" in query or "Temperatura" in query:
            from engine.features import clima
            clima(query)

        elif "no youtube" in query or "no YouTube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "horas" in query or "horario" in query or "Horas" in query or "horário" in query:
            from engine.features import hora
            hora(query)
            
        elif "calendário" in query or "Calendário" in query or "calendario" in query or "Calendario" in query:
            from engine.features import calendario
            calendario(query)

        # Inicialização do navegador
        elif "abrir navegador" in query or "Abrir navegador" in query:
            localizaçãoN = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
            Word = subprocess.Popen(localizaçãoN)

        # Inicialização do bloco de notas
        elif 'abrir bloco de notas' in query or "Abrir bloco de notas" in query:
            speak("Abrindo o bloco de notas")
            localização = "C:/WINDOWS/system32/notepad.exe"
            notepad = subprocess.Popen(localização)

        # Abrir o Word
        elif 'abrir word' in query or "Abrir word" in query:
            speak("Abrindo o Word")
            localizaçãoW = "C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"
            Word = subprocess.Popen(localizaçãoW)

        # Iniciar o PowerPoint
        elif 'abrir powerpoint' in query or "Abrir powerpoint" in query:
            speak("Abrindo o PowerPoint")
            localizaçãoP = "C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE"
            powerpoint = subprocess.Popen(localizaçãoP)

        elif "Canva" in query:
            speak("Abrindo Canva")
            chromepath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            pesquisa = "Canva"
            wb.get(chromepath).open_new_tab(pesquisa + ".com")

        elif "Musica" in query:
            url = "https://www.youtube.com/watch?v=KMTo2LmixqQ"
            chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            wb.get(chrome_path).open(url)

        # PyAutoGui características
        elif "esconder menu" in query:
            # Win + X: Abre o menu escondido do Windows
            pyautogui.hotkey('winleft', 'x')

        elif 'gerenciador de tarefas' in query:
            # Ctrl + Shift + Esc: Abre o Gerenciador de Tarefas
            pyautogui.hotkey('ctrl','shift','esc')
            
        elif "exibir tarefas" in query:
            # Win + Tab: Abre todas as janelas e processos no computador
            pyautogui.hotkey('winleft', 'tab')

        elif "print" in query:
            # Win + PrtScr: Faz uma captura de tela
            pyautogui.hotkey('winleft', 'prtscr')
            speak("Pronto")
            
        elif "recorte" in query:
            # Win + Shift + S: Abre a ferramenta de recorte
            pyautogui.hotkey('winleft', 'shift', 's')

        # Pode ser qualquer aplicativo, pois está no atalho Alt + F4 que encerra o programa
        elif "fechar aplicativo" in query:
            # Alt + F4: Fecha o aplicativo ativo
            pyautogui.hotkey('alt', 'f4')

        elif "nova área de trabalho" in query:
            # Win + Ctrl + D: Cria uma nova área de trabalho
            pyautogui.hotkey('winleft', 'crtl', 'd')
            
        elif "configurações" in query:
            # Win + I: Abre as Configurações do Windows
            pyautogui.hotkey('winleft', 'i')

        # Verifica se o comando está nos comandos de web salvos no banco de dados
        elif query in web_commands:
            print(f"Executando comando de web: {query}")
            wb.open(web_commands[query])
            speak(f"Abrindo {query}")

        # Verifica se o comando está nos comandos do Windows salvos no banco de dados
        elif query in windows_commands:
            try:
                subprocess.Popen(windows_commands[query])
                speak(f"Abrindo {query}")
            except FileNotFoundError:
                speak(f"Não consegui encontrar o arquivo para {query}. Verifique o caminho.")
            except Exception as e:
                speak(f"Ocorreu um erro ao abrir {query}: {str(e)}")

        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("Erro ao processar o comando.")
    
    eel.ShowHood()

# Inicializa o Eel, que é uma biblioteca para criar aplicações GUI usando web technologies
eel.init('web')
