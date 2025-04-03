import csv
import sqlite3

# Conecta-se ao banco de dados SQLite chamado "IVE.db"
con = sqlite3.connect("IVE.db")

# Cria um objeto cursor para executar comandos SQL no banco de dados
cursor = con.cursor()

# Define uma consulta SQL para criar uma tabela chamada "sys_command"
# A tabela terá três colunas:
# - id: uma chave primária do tipo inteiro
# - name: uma coluna para armazenar o nome, com um tamanho máximo de 100 caracteres
# - path: uma coluna para armazenar o caminho, com um tamanho máximo de 10000 caracteres
query = """
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(10000)
)
"""

# Executa a consulta SQL para criar a tabela, se ela ainda não existir
cursor.execute(query)

# O código para fechar a conexão com o banco de dados não está incluído aqui,
# mas é uma boa prática fechar a conexão quando terminar as operações.
# Exemplo: con.close()
