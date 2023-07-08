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
line = 0
column = 0
lline = 0
lcolumn = 0

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

def error_handler(row: int, a, action, sb):
  global lline, lcolumn
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
    print(f"Warning! Sintaxe inesperada: '{a['class']}', linha {lline}, coluna {lcolumn}. Opcao permitida: '{correct_options[0]}'.")
    return 'Fix', fix_map[correct_options[0]]
  elif len(correct_options) == 1 and correct_options[0] in sb:
    print(f"Warning! Sintaxe inesperada: '{a['class']}', linha {lline}, coluna {lcolumn}. Opcao permitida: '{correct_options[0]}'.")
    return 'Fix', correct_options[0]
  else:
    print(f"Panic! Sintaxe inesperada: '{a['class']}', linha {lline}, coluna {lcolumn}. Opcoes permitidas: {correct_options}")
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


def step(action_goto, a, fix=False, next_a=None):
    global s, t, stack, line, column, lline, lcolumn
    s = stack_top()
    var_action = find_action(action_goto, s, a)

    if var_action[0] == 'S':
        # empilhe p na pilha
        t = var_action[1:]
        stack.append(int(t))

        if not fix:
            lline = line
            lcolumn = column
            a, line, column = scanner()
        else:
            a = next_a

    elif var_action[0] == 'R':
        var_rule = find_rule(var_action[1:])

        #desempilha beta times
        var_size_beta = len(var_rule[1:])
        stack_pop_beta_times(var_size_beta)

        # faça t ser o topo da pilha
        t = stack_top()
        #empilhe goto[t, A]
        var_goto = find_go_to(action_goto, t, var_rule[0])
        stack.append(var_goto)

        #Imprima A -> B (imprimir direito dps)
        print_rule(var_rule)
    return var_action, a

def analysis(action_goto):
    global s, t, stack, line, column, lline, lcolumn
    lline = line
    lcolumn = column
    a, line, column = scanner()

    while 1:
        var_action, a = step(action_goto, a)

        if var_action == "Acc":
            # tirar o print e retornar None
            return "done"
        elif var_action == "nan":
            # return None
            error_type, correct_input = error_handler(s, a, action_goto, symbol_table)
            if (error_type == 'Fix'):
                correct_a = {'class': correct_input}
                # chama a funcao analysis com o novo a
                var_action, a = step(action_goto, correct_a, fix=True, next_a=a)
            else:
                return None


def parser():
    action_goto = open_file()

    analysis(action_goto)

    return 1
