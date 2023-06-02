from structures import *
from service import *
import json


# if __name__ == '__main__':
#     text = open_file('programa.p')
#     scanner(text)
#     print(json.dumps(symbol_table, indent=4))

def main():
    while 1:
        token = scanner()
        if not token:
            break
        print(token)

    # print("------------- TABELA DE SIMBOLOS -----------------")
    # print(json.dumps(symbol_table, indent=4))
    return

main()
