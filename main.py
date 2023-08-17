from parser.parser import parser
from scanner.scanner import scanner
from parser.semantic_rules import *
def main():
    #choose_semantic_rule({'lexeme': 'B', 'class': 'id', 'type': 'Nulo'}, 8, 1, {})
    parser()

    return

main()
