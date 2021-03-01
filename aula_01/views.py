from utils import load_data, load_template
import urllib

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

        print('\nPARAMS: ')
        print(params)

        notes_li = [
            note_template.format(title=dados['titulo'], details=dados['detalhes'])
            for dados in list(params)
        ]
        notes = '\n'.join(notes_li)

        return load_template('index.html').format(notes=notes).encode()

    else:
        # Cria uma lista de <li>'s para cada anotação
        # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        notes_li = [
            note_template.format(title=dados['titulo'], details=dados['detalhes'])
            for dados in load_data('notes.json')
        ]
        notes = '\n'.join(notes_li)

        return load_template('index.html').format(notes=notes).encode()