# Importa o módulo "os" para interagir com o sistema operacional
import os

# Importa o módulo "eel" para criar a interface gráfica web
import eel

# Importa todas as funções do módulo "engine.features"
from engine.features import *

# Importa todas as funções do módulo "engine.command"
from engine.command import *


# Define a função "start"
def start():

    # Inicializa o "eel" na pasta "www"
    eel.init("www")

    # Executa o comando para abrir o Microsoft Edge no modo aplicativo, abrindo a URL da interface do I.V.E.
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Inicia o servidor web do "eel", servindo o arquivo "index.html", rodando em "localhost" e bloqueando a execução até que o servidor seja fechado.
    eel.start('index.html', mode=None, host='localhost', block=True)