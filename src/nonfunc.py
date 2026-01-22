import threading as thread
import time
import db
modecountdown=30
mode=1
countdown=1
#Checking 
def monitor():
    while True:
        #sleep half an hour and check mode
        time.sleep(0.1*10)
        modeswitch()
        checkmode()

def modeswitch():
    global modecountdown
    global mode
    modecountdown=modecountdown-1
    if modecountdown==0:
        mode=0
        logs.newlog(0,"Now in inactive mode")
        print("mode switched")
        


def checkmode():
    global countdown
    if countdown!=0:
        countdown=countdown-1
    else:
        countdown=30
        if mode==1:
            db.getallbooks()
            db.getallprofile()
            print("currently Active mode")
            print("routine DB update")

if __name__=="__main__":
    monitor()
