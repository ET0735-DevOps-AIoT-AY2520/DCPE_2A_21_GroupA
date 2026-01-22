import threading as thread
import time
import db

countdown=1
#Checking 
def monitor():
    while True:
        #sleep half an hour and check mode
        time.sleep(0.1*10)
        checkmode()

def checkmode():
    global countdown
    if countdown!=0:
        countdown=countdown-1
        print("Currently in inactive, do nothing")
    else:
        countdown=30
        print("currently Active mode")
        print("routine DB update")

if __name__=="__main__":
    monitor()
