from structures import *

token_list = []
text = ""
line = 0
column = 0
count = 0
def open_file():
    global text
    f = open('programa.p')
    text = f.read()
    return
def take_symbol_and_def(count):
    if count == len(text):
        return "EOF", "EOF"

    return text[count], find_symbol_def(text[count])

def last_column():
    return line < len(text) and column == len(text[line])

def update_column_and_line(symbol, state):
    global line, column
    column += 1
    if symbol == ignored_char[2] and state != 18 and state != 20:
        column = 0
        line += 1
    return

def add_symbol_to_lexeme(symbol, lexeme, state):
    if symbol in ignored_char and state != 18 and state != 20:
        return lexeme

    return lexeme + symbol
def scanner():
    global line, column, count
    if len(text) == 0:
        open_file()

    state = 1
    lexeme = ""
    token = None
    while count <= len(text):
        symbol, symbol_def = take_symbol_and_def(count)

        lexeme = add_symbol_to_lexeme(symbol, lexeme, state)

        state = afd(symbol_def, state)

        next_symbol = "" if count >= len(text) - 1 else text[count + 1]

        if not afd(find_symbol_def(next_symbol), state) or count == len(text) - 1:
            token = tokenization(lexeme, symbol_def, state)
            count += 1
            update_column_and_line(symbol, state)
            break

        count += 1
        update_column_and_line(symbol, state)


    return token

def afd(current_class, current_state):
    if (current_class not in state_dict) or (current_state not in state_dict[current_class]):
        return 0
    return state_dict[current_class][current_state]

def find_class(lexeme, state):
    if lexeme in symbol_table:
        return lexeme

    return language_class[state]

def find_type(state):
    if state not in language_type:
        return "Nulo"

    return language_type[state]

def symbol_table_update(lexeme, token):
    if lexeme not in symbol_table:
        symbol_table[lexeme] = token

    return symbol_table[lexeme]

def show_error_message(state):
    if(state == 1):
        print("ERRO: Arquivo Vazio")
    if(state == 18):
        print("ERRO: Literal incompleto")
    if(state == 20):
        print("ERRO: Comentário incompleto")
    if state == 4 or state == 6 or state == 8:
        print("ERRO: Número incompleto")
    if state == 24:
        print("ERRO: Caractere inválido na linguagem, linha " + str(line) + ", coluna " + str(column))

def tokenization(lexeme, symbol_def, state):
    token_class = find_class(lexeme, state)
    token_type = find_type(state)
    token = {"lexeme": lexeme, "class": token_class, "type": token_type}
    if token_class == "id":
        token = symbol_table_update(lexeme, token)
    if(token_class == "ERRO"):
        show_error_message(state)

    return token

def find_symbol_def(symbol):
    if symbol in letter:
        if symbol == 'E' or symbol == 'e':
            return "Ee"
        return "letter"

    if symbol in digit:
        return "digit"

    if symbol in ignored_char:
        return "ignored_char"

    if symbol in especial_char:
        return symbol

    return "invalid_char"

