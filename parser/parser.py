import queue
import pandas as pd
from scanner.scanner import scanner
from parser.structures import *

goto = []
q = queue.Queue() #can use as stack with get() and put()
q.put(0)
beta = None
t = None
s = 0

def open_file():
    action = pd.read_csv('parser/Action.csv')
    go_to = pd.read_csv('parser/goto.csv')
    print(action.loc[0].at["inicio"])
    return action, go_to

def find_on_go_to_table(t):
    return rules[t]

def queue_pop_beta_times(var_size_beta):
    global q
    while var_size_beta:
        q.get()
        var_size_beta -= 1

    return None

def analysis(a, action, go_to):
    global s, t, q
    qlist = q.queue
    print("qlist foi? " + str(qlist))
    s = qlist[len(qlist) - 1]
    print("stack at beginning: " + str(qlist))
    print("a -> " + str(a))
    print("s -> " + str(s) + ", a[class] -> " + str(a["class"]))
    var_action = action.loc[s].at[a["class"]]
    if var_action[0] == 'S':
        t = var_action
        print("t -> " + str(t))
        q.put(int(t[1:]))
        return "shift " + str(t[1:])

    if action.loc[s].at[a["class"]][0] == 'R':
        print("tá na hora de reduzir padin?")
        var_rule = find_on_go_to_table(t[1:])
        print("var_rule -> " + str(var_rule))
        var_size_beta = len(var_rule[1:])
        queue_pop_beta_times(var_size_beta)
        qlist = q.queue
        t = qlist[len(qlist) - 1]
        print("viado o a -> " + str(a["class"]) + ", e o t -> " + str(t))
        q.put(int(go_to.loc[t].at[var_rule[0]]))
        print(str(var_rule[0] + "-> " + var_rule[1:]))

    if t == "acc":
        return "done"

    else:
        return "eltin bota rotina de erro aqui pra nois"

def parser():
    action, go_to = open_file()

    token = {"lexeme": "", "class": "", "type": ""}

    while token:
        token = scanner()
        print(analysis(token, action, go_to))

    return 1
