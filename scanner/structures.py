import string

digit = [str(x) for x in list(range(0,10))]

letter = list(string.ascii_letters)

especial_char = [",", ";", ".",
                   "*" ,"+" ,"-" , "/" , "(", ")", "{", "}",
                  "<" , ">", "=", '"', "_"]

# literal_char = [":", "!", "?", "\\", "[", "'"]

ignored_char = ['\t', ' ', '\n', ""]

symbol_table = {
    "inicio": {
        "lexeme": "inicio",
        "class": "inicio",
        "type": "inicio"
    },
    "varinicio": {
        "lexeme": "varinicio",
        "class": "varinicio",
        "type": "varinicio"
    },"varfim": {
        "lexeme": "varfim",
        "class": "varfim",
        "type": "varfim"
    },"escreva": {
        "lexeme": "escreva",
        "class": "escreva",
        "type": "escreva"
    },"leia": {
        "lexeme": "leia",
        "class": "leia",
        "type": "leia"
    },"se": {
        "lexeme": "se",
        "class": "se",
        "type": "se"
    },"entao": {
        "lexeme": "entao",
        "class": "entao",
        "type": "entao"
    },"fimse": {
        "lexeme": "fimse",
        "class": "fimse",
        "type": "fimse"
    },"Repita": {
        "lexeme": "Repita",
        "class": "Repita",
        "type": "Repita"
    },"fimRepita": {
        "lexeme": "fimRepita",
        "class": "fimRepita",
        "type": "fimRepita"
    },"fim": {
        "lexeme": "fim",
        "class": "fim",
        "type": "fim"
    },"inteiro": {
        "lexeme": "inteiro",
        "class": "inteiro",
        "type": "inteiro"
    },"literal": {
        "lexeme": "literal",
        "class": "literal",
        "type": "literal"
    },"real": {
        "lexeme": "real",
        "class": "real",
        "type": "real"
    },
}

state_dict = {
    "letter":{
        1:2, 2:2, 18:18, 20:20
    },
    "digit":{
        1:3, 2:2, 3:3, 4:5, 5:5, 6:7, 7:7, 8:7, 18:18, 20:20
    },
    ".":{
        3:4, 18:18, 20:20
    },
    "Ee":{
        1:2, 2:2, 3:6, 5:6, 18:18, 20:20
    },
    "_":{
        2:2, 18:18, 20:20
    },
    "+":{
        1:13, 6:8, 18:18, 20:20
    },
    "-":{
        1:13, 6:8, 11:12, 18:18, 20:20
    },
    ">":{
        1:9, 11:10, 18:18, 20:20
    },
    "=":{
        1:10, 11:10, 18:18, 20:20
    },
    "<":{
        1:11, 18:18, 20:20
    },
    "*":{
        1:13, 18:18, 20:20
    },
    "/":{
        1:13, 18:18, 20:20
    },
    "(":{
        1:14, 18:18, 20:20
    },
    ")":{
        1:15, 18:18, 20:20
    },
    ";":{
        1:16, 18:18, 20:20
    },
    ",":{
        1:17, 18:18, 20:20
    },
    '"':{
        1:18, 18:19, 20:20
    },
    '{':{
        1:20, 18:18, 20:20
    },
    "}":{
        18:18, 20:1
    },
    "EOF":{
        1:22
    },
    "literal_char":{
        18:18, 20:20
    },
    "ignored_char":{
        1:1, 18:18, 20:20
    },
    "invalid_char":{
        1:23, 18:18, 20:20
    }
}

language_class = {
    2: "id",
    3: "Num",
    5: "Num",
    7: "Num",
    9: "OPR",
    10: "OPR",
    11: "OPR",
    12: "RCB",
    13: "OPM",
    14: "AB_P",
    15: "FC_P",
    16: "PT_V",
    17: "Vir",
    19: "Lit",
    21: "Comentário",
    22: "EOF",
    0: "ERRO",
    1: "ERRO",
    4: "ERRO",
    6: "ERRO",
    8: "ERRO",
    18: "ERRO",
    20: "ERRO",
    23: "ERRO",
}

language_type = {
    3: "inteiro",
    5: "real",
    7: "real"
}
