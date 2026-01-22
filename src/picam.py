from threading import Thread
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
import cv2
from time import sleep
import sys
import queue
import nonfunc as mode
barcode_queue = queue.Queue()

def scanner_loop():
   
    # Initialize Picamera2 (Source [2])
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (1640, 1232)})
    picam2.configure(config)
    picam2.start()

    sleep(1)
    #pass the camera to function

    singleframe(picam2)
    while True:
        frame = picam2.capture_array()
        #https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        barcodes = decode(gray)

        if len(barcodes) > 0:
            data = barcodes[0].data.decode("utf-8")
            print("Detected:", data)
            logs.newlog(0,"Switched to Active mode")
            mode.mode=1
            mode.modecountdown=30
            barcode_queue.put(data)  # send barcode to main program
            sleep(2)  # small delay to avoid double reads
        sleep(0.1)




def start_scanner():
    
    #good practice to set daemon = true https://www.geeksforgeeks.org/python/python-daemon-threads/
    
    thread = Thread(target=scanner_loop, daemon=True)
    thread.start()


def timeout():
    sleep(5)
    #create a flag global 
    global outflag
    outflag=1
    
# SELFIE MODE
def singleframe(picam2):
    frame = picam2.capture_array()

    # Save a selfie LMAO
    cv2.imwrite("single_frame.jpg", frame)

    print("Saved single_frame.jpg")


