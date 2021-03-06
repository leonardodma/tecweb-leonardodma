  
from utils import load_data, load_template, build_response
import urllib
import json


def write_json(data, filename='data/notes.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, ensure_ascii=False, indent=4) 


def index(request):
    note_template = load_template('components/note.html')

    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]

        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        
        for chave_valor in corpo.split('&'):
            # AQUI É COM VOCÊ
            unquote = urllib.parse.unquote_plus(chave_valor).split('=')
            params[unquote[0]] = unquote[1]

        print('\n----------PARAMS -------------')
        print(params)
        print('\n-------------------------------')


        with open('data/notes.json') as json_file:
            data = json.load(json_file)
        
        data.append(params)
        write_json(data)

        return build_response(code=303, reason='See Other', headers='Location: /')


    else:
        # Cria uma lista de <li>'s para cada anotação
        # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        notes_li = [
            note_template.format(title=dados['titulo'], details=dados['detalhes'])
            for dados in load_data('notes.json')
        ]
        notes = '\n'.join(notes_li)

        return build_response() + load_template('index.html').format(notes=notes).encode()