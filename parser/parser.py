import collections
import pandas as pd
from scanner.scanner import scanner
from parser.structures import *
from scanner.structures import symbol_table
df = None
stack = collections.deque([0])
beta = None
t = None
s = 0

def open_file():
    action_goto = pd.read_csv('parser/action_goto.csv')
    return action_goto

def find_rule(rule):
    return rules[rule]

def stack_pop_beta_times(var_size_beta):
    global stack
    while var_size_beta:
        stack.pop()
        var_size_beta -= 1

    return None

def print_rule(var_rule):
    print(var_rule[0] + " ->", end="")
    count = 1
    while count < len(var_rule):
        print(" " + var_rule[count], end="")
        count += 1
    print("")
    return None

def stack_top():
    return stack[-1]

def find_action(action, s, a):
    return str(action.loc[s].at[a["class"]])

def find_go_to(action_goto, t, var_rule):
    return int(action_goto.loc[t].at[var_rule])

def error_handler(row: int, column: str, action, sb):
  fix_map = {
      ';':'pt_v',
      '(': 'ab_p',
      ')': 'fc_p',
      'entao': 'entao',
      '<-': 'rcb',
      ',': 'vir',
  }
  correct_options = get_correct_options(row, action)
  if len(correct_options) == 1 and correct_options[0] in fix_map:
    return 'Fix', fix_map[correct_options[0]]
  elif len(correct_options) == 1 and correct_options[0] in sb:
    return 'Fix', correct_options[0]
  else:
    print(f"Sintaxe inesperada: '{column}'. Opcoes permitidas: {correct_options}")
    return 'Panic', None

def get_correct_options(row_index, action):
    type_map = {
          'pt_v': ';',
          'id': 'identificador',
          'vir': ',',
          'lit': 'constante literal',
          'num': 'constante numerica',
          'rcb': '<-',
          'opm': 'operador aritmetico',
          'ab_p': '(',
          'fc_p': ')',
          'opr': 'operador relacional'
    }
    empty_columns = []
    row = action.iloc[row_index]
    for column in action.columns:
        if (column == '$'): break
        if (not pd.isnull(row[column])):
            if(column in type_map):
                empty_columns.append(type_map[column])
            else:
                empty_columns.append(column)
    return empty_columns

def analysis(action_goto):
    global s, t, stack
    a = scanner()
    print("#    TOKEN: " + str(a) + "                 #")

    while 1:
        s = stack_top()
        var_action = find_action(action_goto, s, a)
        print("s -> " + str(s) + ", aclass -> " + str(a["class"]) + ", varaction -> " + str(type(var_action)))

        if var_action[0] == 'S':
            # empilhe p na pilha
            t = var_action[1:]
            stack.append(int(t))
            print("shift " + t)

            a = scanner()
            print("#    TOKEN: " + str(a) + "                 #")

        elif var_action[0] == 'R':
            var_rule = find_rule(var_action[1:])

            #desempilha beta times
            var_size_beta = len(var_rule[1:])
            stack_pop_beta_times(var_size_beta)

            # faça t ser o topo da pilha
            t = stack_top()
            #empilhe goto[t, A]
            print("t: " + str(t) + ", A: " + str(var_rule[0]), end = "")
            var_goto = find_go_to(action_goto, t, var_rule[0])
            stack.append(var_goto)
            print(", go_to " + str(var_goto))

            #Imprima A -> B (imprimir direito dps)
            print_rule(var_rule)

        elif var_action == "Acc":
            # tirar o print e retornar None
            return "done"

        else:
            return None
            # error_type, fixed_input = error_handler(s, a, action_goto, symbol_table)
            # if (error_type == 'Fix'):
            #     print(f"{error_type} | {fixed_input}")
            #     # chama a funcao analysis com o novo a
            # else:
            #     print(f"{error_type}!")
            #     return None


def parser():
    action_goto = open_file()

    print(analysis(action_goto))

    return 1
