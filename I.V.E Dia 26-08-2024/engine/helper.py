import re

def extract_yt_term(command):
    """
    Extrai o termo do YouTube de um comando, assumindo que o termo está
    formatado como ' ... TERM no youtube'.

    Parâmetros:
    command (str): O comando de entrada contendo o termo do YouTube.

    Retorna:
    str ou None: O termo extraído se encontrado, caso contrário, None.
    """
    # Define a expressão regular para capturar o termo entre espaços e seguido de 'no youtube'
    pattern = r'\s+(.*?)\s+no\s+youtube'
    
    # Usa re.search para encontrar o termo no comando, ignorando maiúsculas e minúsculas
    match = re.search(pattern, command, re.IGNORECASE)
    
    # Se um termo for encontrado, retorna o termo extraído; caso contrário, retorna None
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    """
    Remove palavras indesejadas de uma string.

    Parâmetros:
    input_string (str): A string de entrada da qual palavras serão removidas.
    words_to_remove (list of str): Lista de palavras a serem removidas da string.

    Retorna:
    str: A string com as palavras removidas.
    """
    # Divide a string de entrada em palavras individuais
    words = input_string.split()
    
    # Filtra palavras removendo aquelas que estão na lista words_to_remove
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    
    # Junta as palavras restantes de volta em uma string
    result_string = ' '.join(filtered_words)
    
    return result_string
