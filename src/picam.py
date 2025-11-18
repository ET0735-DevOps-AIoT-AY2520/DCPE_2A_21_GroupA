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
    frame = picam2.capture_array()

    # Save a selfie LMAO
    cv2.imwrite("single_frame.jpg", frame)
    picam2.stop()
    print("Saved single_frame.jpg")

  


    




