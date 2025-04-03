import os
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import datetime
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
import webbrowser as wb
import requests
from engine.helper import extract_yt_term, remove_words

# Chave de API para OpenWeatherMap
key_clima = "Colocar chave do clima aqui!!!!!!"

# Importa e configura a API do Google Generative AI
import google.generativeai as genai
API_KEY = 'Colocar chave do dev.gemini aqui!!!!'
genai.configure(api_key=API_KEY)

# Conecta-se ao banco de dados SQLite
con = sqlite3.connect("IVE.db")
cursor = con.cursor()

@eel.expose
def openCommand(query):
    """
    Abre um aplicativo ou site com base no comando recebido.
    
    Parâmetros:
    query (str): Comando para abrir um aplicativo ou site.
    """
    # Remove o nome do assistente e o comando de abertura da consulta
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("abra", "")
    query = query.lower()
    
    # Obtém o nome do aplicativo ou site
    app_name = query.strip()

    if app_name != "":
        try:
            # Tenta encontrar o caminho do aplicativo no banco de dados
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Abrindo " + query)
                os.startfile(results[0][0])
            else:
                # Se não encontrar o caminho, tenta encontrar a URL do site
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Abrindo " + query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Abrindo " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("Não encontrado")
        except:
            speak("Something went wrong")

def PlayYoutube(query):
    """
    Reproduz um vídeo no YouTube baseado na consulta.
    
    Parâmetros:
    query (str): Comando para reproduzir um vídeo no YouTube.
    """
    search_term = extract_yt_term(query)
    speak("Tocando " + search_term + " no YouTube")
    kit.playonyt(search_term)

def hora(query):
    """
    Fala a hora atual.
    
    Parâmetros:
    query (str): Comando para obter a hora.
    """
    agora = datetime.datetime.now()
    hora_atual = agora.strftime("%H:%M:%S")
    hora_texto = agora.strftime("%H Horas e %M minutos e %S segundos")
    speak("A hora atual é " + hora_texto)
    print(hora_atual)

def calendario(query):
    """
    Fala a data atual.
    
    Parâmetros:
    query (str): Comando para obter a data.
    """
    dia = int(datetime.datetime.now().day)
    mes = int(datetime.datetime.now().month)
    ano = int(datetime.datetime.now().year)
    speak('O dia de hoje é {}/{}/{}'.format(dia, mes, ano))

def Abrir_navegador(query):
    """
    Abre o navegador Microsoft Edge.
    
    Parâmetros:
    query (str): Comando para abrir o navegador.
    """
    url = ""
    navegador_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    wb.get(navegador_path).open(url)

def clima(query):
    """
    Obtém e fala a previsão do clima para uma cidade específica.
    
    Parâmetros:
    query (str): Comando para obter o clima.
    """
    cidade = "Araraquara"

    # URL para obter dados do clima
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key_clima}&units=metric"

    # Faz a solicitação HTTP
    response = requests.get(url)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        # Processa os dados recebidos
        dados = response.json()
        print("JSON response:", dados)
        temperatura = dados["main"]["temp"]
        descricao = dados["weather"][0]["description"]
        speak(f"A temperatura atual em {cidade} é {temperatura}°C.")
    else:
        erro_mensagem = response.json().get("message", "Unknown error")
        speak(f"Erro ao obter os dados do clima: {erro_mensagem}")

def hotword():
    """
    Escuta por palavras-chave pré-definidas e executa uma ação quando detectadas.
    """
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Configura o detector de palavras-chave
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa", "ive"]) 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        # Loop para escutar continuamente
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detectado")

                # Pressiona a combinação de teclas Win + J
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"um error aconteceu: {e}")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def chatBot(query):
    """
    Gera uma resposta de um chatbot baseado na consulta.
    
    Parâmetros:
    query (str): Comando ou pergunta para o chatbot.
    """
    user_input = query.lower()
    geminiModel = genai.GenerativeModel("gemini-pro")
    response = geminiModel.generate_content(user_input)
    print(response.text)
    speak(response.text)
    eel.receiverText(response.text)
    return response
