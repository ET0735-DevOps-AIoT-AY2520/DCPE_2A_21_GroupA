from threading import Thread
from picamera2 import Picamera2
from pyzbar.pyzbar import decode
import cv2
from time import sleep
import sys
import queue

barcode_queue = queue.Queue()

def runcam():
   
    # Initialize Picamera2 
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (1640, 1232)})
    picam2.configure(config)
    picam2.start()

    sleep(1)

    # Save a selfie LMAO
    singleframe(picam2) #Moved to a seperate function

    while True:
        frame = picam2.capture_array()
        #https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        # if a barcode has been detetced
        if len(barcodes) > 0:
            data = barcodes[0].data.decode("utf-8")
            print("Detected:", data)
            barcode_queue.put(data)  # send barcode into queue
            sleep(2)  # small delay to avoid double reads
        sleep(0.1)

  

# SELFIE MODE
def singleframe(picam2):
    frame = picam2.capture_array()

    # Save a selfie LMAO
    cv2.imwrite("single_frame.jpg", frame)

    print("Saved single_frame.jpg")



    




