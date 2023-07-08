import collections
import pandas as pd
from scanner.scanner import scanner
from parser.structures import *

goto = []
stack = collections.deque([0])
beta = None
t = None
s = 0

def open_file():
    action = pd.read_csv('parser/Action.csv')
    go_to = pd.read_csv('parser/goto.csv')
    return action, go_to

def find_on_go_to_table(rule):
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

def analysis(action, go_to):
    global s, t, stack
    a = scanner()

    while 1:
        s = stack[-1]
        var_action = action.loc[s].at[a["class"]]
        print("s -> " + str(s) + ", aclass -> " + str(a["class"]) + ", varaction -> " + var_action)
        if var_action[0] == 'S':
            # empilhe p na pilha
            t = var_action[1:]
            stack.append(int(t))
            print("shift " + t)

            a = scanner()

        elif var_action[0] == 'R':
            var_rule = find_on_go_to_table(var_action[1:])

            #desempilha beta times
            var_size_beta = len(var_rule[1:])
            stack_pop_beta_times(var_size_beta)

            # faça t ser o topo da pilha
            t = stack[-1]
            #empilhe goto[t, A]
            var_goto = int(go_to.loc[t].at[var_rule[0]])
            stack.append(var_goto)
            print("go_to " + str(var_goto))

            #Imprima A -> B (imprimir direito dps)
            print_rule(var_rule)

        elif var_action == "Acc":
            return "done"

        else:
            return "eltin bota rotina de erro aqui pra nois"

def parser():
    action, go_to = open_file()

    print(analysis(action, go_to))

    return 1
