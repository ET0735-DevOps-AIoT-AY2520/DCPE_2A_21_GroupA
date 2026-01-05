import datetime

logs=[]

def logsinit():
    global logs
    logs=[]

def newlog(type,msg):
    global logs
    now=datetime.datetime.now()
    types={
        1:"READ",
        2:"WRITE",
        3:"LOGIN",
        4:"INPUT",
        5:"OUTPUT",
        6:"WARN",
        7:"ERROR",
    }
    logs.append("["+types[type]+"]["+str(now)+"]"+msg)
    print(logs[0])
    