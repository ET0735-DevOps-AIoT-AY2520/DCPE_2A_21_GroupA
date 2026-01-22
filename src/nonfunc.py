import threading as thread
import time

mode=0
#Checking 
def monitor():
    print("checking")
    #sleep half an hour and check mode
    time.sleep(0.1*60)
    mode()


def mode():
    global mode
    if mode==0:
        print("Currently in inactive, do nothing")
    else:
        print("currently Active mode")
        print("routine DB update")

if __name__=="__main__":
    monitor()
