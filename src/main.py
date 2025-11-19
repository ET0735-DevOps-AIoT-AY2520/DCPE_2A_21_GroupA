import time
from threading import Thread
import queue

import db as db
import picam as picam

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_keypad as keypad
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_input_switch as input_switch
from hal import hal_ir_sensor as ir_sensor
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_usonic as usonic
from hal import hal_dc_motor as dc_motor
from hal import hal_accelerometer as accel






#Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    global currentkey
    currentkey=key
    time.sleep(1)
    currentkey="z"





def main():
    global currentkey
    currentkey="z"
    print("test")
    lcd = LCD.lcd()
    lcd.lcd_clear()


    # Display something on LCD
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)
    picam.start_scanner()
    # Initialize the HAL keypad driver
    keypad.init(key_pressed)

    # Start the keypad scanning which will run forever in an infinite while(True) loop in a new Thread "keypad_thread"
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    caminput="0"
    while True:
        caminput=picam.barcode_queue.get()
        if caminput != "0": 
            gotmatch(caminput)
            while not picam.barcode_queue.empty():
                picam.barcode_queue.get_nowait()
        time.sleep(1)


def gotmatch(caminput):
    lcd=LCD.lcd()
    db.getallbooks()
    db.getallprofile()
    global profileadm
    profileadm=db.matchprofile(caminput)
    print(profileadm)
    if profileadm!="":
        lcd.lcd_clear()
        lcd.lcd_display_string("1-Collect Books",1)
        lcd.lcd_display_string("2-Return Books",2)
        while True:
            if currentkey== 1:
                print("collect books")
                collectbooks()
                break
            elif currentkey ==2:
                print("return books")
                returnbooks()
                break
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("No Account",1)
        lcd.lcd_display_string("Found",2)
        time.sleep(1)
        
def collectbooks():
    lcd=LCD.lcd()
    global profileadm
    gotfine = 0
    print("going in check fine")
    gotfine = db.checkfines(profileadm) #add func here
    print(gotfine)
    print(type(gotfine))
    if gotfine!=0:
        lcd.lcd_clear()
        lcd.lcd_display_string("Pls Tap Card to",1)
        lcd.lcd_display_string("pay $"+gotfine,2)
        while True:
            time.sleep(10)
            break
            #wait for RFID and deduct money here

def returnbooks():
    print("return books")

if __name__ == '__main__':
    main()