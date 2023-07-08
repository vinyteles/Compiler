from scanner.structures import *

token_list = []
text = ""
line = 1
column = 1
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
        column = 1
        line += 1
    return

def is_ignored_char(symbol, state):

    return symbol in ignored_char and state != 18 and state != 20

def is_comentary(symbol, state):
    return state == 20 and symbol == '}'

def update_lexeme(symbol, lexeme, state):
    if is_ignored_char(symbol, state):
        return lexeme

    if is_comentary(symbol, state):
        return ''

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

        lexeme = update_lexeme(symbol, lexeme, state)

        state = afd(symbol_def, state)

        next_symbol = "" if count >= len(text) - 1 else text[count + 1]

        if not afd(find_symbol_def(next_symbol), state):
            token = tokenization(lexeme, symbol_def, state)
            count += 1
            update_column_and_line(symbol, state)
            break

        count += 1
        update_column_and_line(symbol, state)


    return token, line, column

def afd(current_class, current_state):
    if (current_class not in state_dict) or (current_state not in state_dict[current_class]):
        return 0
    return state_dict[current_class][current_state]

def find_class(lexeme, state):
    if lexeme in symbol_table:
        return symbol_table[lexeme]["class"]

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
    if(state == 0):
        print("ERRO: Token não reconhecido, linha " + str(line) + ", coluna " + str(column))
    if(state == 1):
        print("ERRO: Arquivo Vazio, linha " + str(line) + ", coluna " + str(column))
    if(state == 18):
        print("ERRO: Literal incompleto, linha " + str(line) + ", coluna " + str(column))
    if(state == 20):
        print("ERRO: Comentário incompleto, linha " + str(line) + ", coluna " + str(column))
    if state == 4 or state == 6 or state == 8:
        print("ERRO: Número incompleto, linha " + str(line) + ", coluna " + str(column))
    if state == 23:
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

