from parser.parser import parser
from scanner.scanner import scanner


def debug_scanner():
    while 1:
        token = scanner()
        print(token)
        if not token:
            break

    return None

def main():

    # debug_scanner()
    parser()

    return

main()
