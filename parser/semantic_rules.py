from collections import deque
from scanner.structures import symbol_table

c_lines = []

def get_c_lines():
    return c_lines

def update_symbol_table(tmplx, type):
    for id in tmplx:
        symbol_table[id]["type"] = type
        #print(symbol_table[id])

    return None

def semantic_stack_pop_beta_times(semantic_stack, var_size_beta):
    while var_size_beta:
        semantic_stack.pop()
        var_size_beta -= 1

    return semantic_stack

def choose_semantic_rule(rule_number, var_rule, var_size_beta, semantic_stack: deque):
    token = {"lexeme": var_rule[0], "class": var_rule[0], "type":"null"}
    # token = eval(f'semantic_rule_{rule_number}({var_rule}, {token}, {var_size_beta}, {semantic_stack.copy()})')
    try:
        token = eval(f'semantic_rule_{rule_number}({var_rule}, {token}, {var_size_beta}, {semantic_stack.copy()})')
    except:
        #print("viado deu erro nos semantics rules: " + rule_number)
        pass
    semantic_stack = semantic_stack_pop_beta_times(semantic_stack, var_size_beta)

    semantic_stack.append(token)

    return semantic_stack

def semantic_rule_0(var_rule, token, var_size_beta, semantic_stack):
    pass

def semantic_rule_1(var_rule, token, var_size_beta, semantic_stack):
    pass

def semantic_rule_2(var_rule, token, var_size_beta, semantic_stack):
    pass

def semantic_rule_3(var_rule, token, var_size_beta, semantic_stack):
    pass
def semantic_rule_4(var_rule, token, var_size_beta, semantic_stack):
    pass

def semantic_rule_5(var_rule, token, var_size_beta, semantic_stack):
    return token, semantic_stack

def semantic_rule_6(var_rule, token, var_size_beta, semantic_stack):
    semantic_stack.pop()
    tmp_l = semantic_stack.pop()
    id_type = semantic_stack.pop()["type"]

    tmplx = tmp_l["lexeme"].split(sep=",")

    for id_lx in tmplx:
        c_lines.append(f'{str(id_type)} {str(id_lx)};\n')

    update_symbol_table(tmplx, id_type)

    return token

def semantic_rule_7(var_rule, token, var_size_beta, semantic_stack):
    tmp_l = semantic_stack.pop()
    tmp_vir = semantic_stack.pop()
    tmp_id = semantic_stack.pop()

    token["lexeme"] = tmp_id["lexeme"] + tmp_vir["lexeme"] + tmp_l["lexeme"]

    return token

def semantic_rule_8(var_rule, token, var_size_beta, semantic_stack):
    tmp_token = semantic_stack.pop()
    token["lexeme"] = tmp_token["lexeme"]

    return token

def semantic_rule_9(var_rule, token, var_size_beta, semantic_stack):
    token["type"] = "int"

    return token

def semantic_rule_10(var_rule, token, var_size_beta, semantic_stack):
    token["type"] = "double"

    return token

def semantic_rule_11(var_rule, token, var_size_beta, semantic_stack):
    token["type"] = "literal"

    return token

def semantic_rule_13(var_rule, token, var_size_beta, semantic_stack):
    semantic_stack.pop()
    token_id = semantic_stack.pop()

    if token_id["lexeme"] in symbol_table:
        if token_id["type"] == "int":
            c_lines.append(f'scanf("%d", &{token_id["lexeme"]});\n')
        elif token_id["type"] == "double":
            c_lines.append(f'scanf("%lf", &{token_id["lexeme"]});\n')
        else:
            c_lines.append(f'scanf("%s", {token_id["lexeme"]});\n')
    else:
        print("Erro, variavel não declarada")
    return token

def semantic_rule_14(var_rule, token, var_size_beta, semantic_stack):

    semantic_stack.pop()
    c_lines.append(f'printf({str(semantic_stack.pop()["lexeme"])});\n')
    return token

def semantic_rule_15(var_rule, token, var_size_beta, semantic_stack):
    token = semantic_stack.pop()

    return token


def semantic_rule_16(var_rule, token, var_size_beta, semantic_stack):
    token = semantic_stack.pop()

    return token

def semantic_rule_17(var_rule, token, var_size_beta, semantic_stack):
    token_id = semantic_stack.pop()
    #print("coe parsero o q tem aq " + str(token_id))
    #print(symbol_table)
    if token_id["lexeme"] in symbol_table and token_id["type"] != "Nulo":
        token = token_id
    else:
        print("Erro! variavel não declarada")
    return token

def semantic_rule_19(var_rule, token, var_size_beta, semantic_stack):
    tmp_ptv = semantic_stack.pop()
    tmp_ld = semantic_stack.pop()
    tmp_rcb = semantic_stack.pop()
    token_id = semantic_stack.pop()

    if token_id["lexeme"] in symbol_table and token_id["type"] != "Nulo":
        token = token_id
    else:
        print("Erro! variavel não declarada")

    c_lines.append(f'{token_id["lexeme"]} {tmp_rcb["lexeme"]} {tmp_ld["lexeme"]}\n')

    return token

def semantic_rule_20(var_rule, token, var_size_beta, semantic_stack):
    tmp_oprd_2 = semantic_stack.pop()
    tmp_opm = semantic_stack.pop()
    tmp_oprd_1 = semantic_stack.pop()
    token["lexeme"] = tmp_oprd_1["lexeme"] + " " + tmp_opm["lexeme"] + " " + tmp_oprd_2["lexeme"]

    return token

def semantic_rule_21(var_rule, token, var_size_beta, semantic_stack):
    tmp_token = semantic_stack.pop()
    token["lexeme"] = tmp_token["lexeme"]
    token["type"] = tmp_token["type"]

    return token

def semantic_rule_22(var_rule, token, var_size_beta, semantic_stack):
    tmp_token = semantic_stack.pop()
    token["lexeme"] = tmp_token["lexeme"]
    token["type"] = tmp_token["type"]

    return token

def semantic_rule_23(var_rule, token, var_size_beta, semantic_stack):
    tmp_token = semantic_stack.pop()
    token["lexeme"] = tmp_token["lexeme"]
    token["type"] = tmp_token["type"]

    return token

def semantic_rule_25(var_rule, token, var_size_beta, semantic_stack):
    c_lines.append("}\n")

    return token

def semantic_rule_26(var_rule, token, var_size_beta, semantic_stack):
    semantic_stack.pop()
    semantic_stack.pop()
    tmp_expr = semantic_stack.pop()

    c_lines.append(f'if({tmp_expr["lexeme"]})')
    c_lines.append("{\n")

    return token

def semantic_rule_27(var_rule, token, var_size_beta, semantic_stack):
    tmp_oprd_2 = semantic_stack.pop()
    tmp_opr = semantic_stack.pop()
    tmp_oprd_1 = semantic_stack.pop()
    token["lexeme"] = tmp_oprd_1["lexeme"] + " " + tmp_opr["lexeme"] + " " + tmp_oprd_2["lexeme"]

    return token

def semantic_rule_32(var_rule, token, var_size_beta, semantic_stack):


    return token

def semantic_rule_33(var_rule, token, var_size_beta, semantic_stack):
    c_lines.append("}\n")

    return token

def semantic_rule_34(var_rule, token, var_size_beta, semantic_stack):
    semantic_stack.pop()
    tmp_expr = semantic_stack.pop()
    c_lines.append(f'while({tmp_expr["lexeme"]})')
    c_lines.append("{\n")

    return token