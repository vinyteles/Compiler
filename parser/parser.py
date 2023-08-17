import collections
import pandas as pd

from parser.semantic_rules import choose_semantic_rule, get_c_lines
from scanner.scanner import scanner
from parser.structures import *
from scanner.structures import symbol_table
df = None
sintatic_stack = collections.deque([0])
semantic_stack = collections.deque()
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

def sintatic_stack_pop_beta_times(var_size_beta):
    global sintatic_stack
    while var_size_beta:
        sintatic_stack.pop()
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

def sintatic_stack_top():
    top_tmp = sintatic_stack[-1]
    return top_tmp

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


def print_semantic_stack(tmp_semantic_stack):
    print("stack beginning -------------------")
    while len(tmp_semantic_stack):

        print("coeee -> " + str(tmp_semantic_stack.pop()))

    print("stack ending -------------------\n")

    return


def step(action_goto, a, fix=False, next_a=None):
    global s, t, sintatic_stack, semantic_stack, line, column, lline, lcolumn
    s = sintatic_stack_top()
    var_action = find_action(action_goto, s, a)
    #print(str(var_action))
    if var_action[0] == 'S':
        t = var_action[1:]
        sintatic_stack.append(int(t))

        if not fix:
            lline = line
            lcolumn = column
            semantic_stack.append(a)
            #print_semantic_stack(semantic_stack.copy())
            a, line, column = scanner()
        else:
            semantic_stack.append(a)
            a = next_a

    elif var_action[0] == 'R':
        rule_number = var_action[1:]
        var_rule = find_rule(rule_number)

        var_size_beta = len(var_rule[1:])
        sintatic_stack_pop_beta_times(var_size_beta)

        t = sintatic_stack_top()
        var_goto = find_go_to(action_goto, t, var_rule[0])
        #print("state " + str(t))
        #print("goto " + str(var_goto))
        sintatic_stack.append(var_goto)
        semantic_stack = choose_semantic_rule(rule_number, var_rule, var_size_beta, semantic_stack)
        #print_semantic_stack(semantic_stack.copy())

    return var_action, a

def analysis(action_goto):
    global s, t, sintatic_stack, line, column, lline, lcolumn
    lline = line
    lcolumn = column
    a, line, column = scanner()
    #print("a -> " + str(a['lexeme']))

    while 1:
        var_action, a = step(action_goto, a)
        if(a['class'] == 'ERRO'):
            a, line, column = scanner()

        if var_action == "Acc":
            return "done"
        elif var_action == "nan":
            error_type, correct_input = error_handler(s, a, action_goto, symbol_table)
            if (error_type == 'Fix'):
                correct_a = {'class': correct_input}
                var_action, a = step(action_goto, correct_a, fix=True, next_a=a)
                if(a['class'] == 'ERRO'):
                    a, line, column = scanner()
            else:
                return False
            
    return True


def parser():
    action_goto = open_file()
    if analysis(action_goto):
        c_lines = get_c_lines()
        c_lines.insert(0, c_beginning)
        c_lines.append(c_ending)

        f = open("programa.c","w")
        indent = 1
        f.write(c_lines[0])

        for line in c_lines[1:]:
            if line[0] == '}':
                indent-=1
            for i in range(indent):
                f.write("  ")
            f.write(line)
            if line[0] == '{':
                indent+=1
        f.close()
        
    return 1
