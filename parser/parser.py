import queue
import pandas as pd

from scanner.scanner import scanner

goto = []
q = queue.Queue()
beta = None
t = None
s = 0

def open_file():
    action = pd.read_csv('parser/Action.csv')
    return action

def analysis(a, action):
    global s, t

    t = action.loc[s].at[a["type"]]

    if t[0] == 's':
        q.put(s)
        return "shift"

    if t[0] == 'R':
        s = q.get()
        t = goto[s][a]
        q.put(t)

    if t == "acc":
        return "done"

    else:
        return "eltin bota rotina de erro aqui pra nois"

def parser():
    action = open_file()

    token = {"lexeme": "", "class": "", "type": ""}

    while token:
        token = scanner()
        print(analysis(token, action))

    return 1
