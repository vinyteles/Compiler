from structures import *
from service import *
import json

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
