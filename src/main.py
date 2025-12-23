import time
from threading import Thread
import queue

import db as db
import picam as picam
import rfid 
import humidity as rh
import servo_motor as sm

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
    rfid.setup()
    led.init()
    # Display something on LCD
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)
    picam.start_scanner()
    # Initialize the HAL keypad driver
    keypad.init(key_pressed)


    #db autoscan
    remres=Thread(target=db.reservationTimeout)
    remres.start()
    # Start the keypad scanning which will run forever in an infinite while(True) loop in a new Thread "keypad_thread"
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    caminput="0"
    while True:
        print("test")
        caminput=picam.barcode_queue.get()
        if caminput != "0": 
            gotmatch(caminput)
            while not picam.barcode_queue.empty():
                #removed anything after the first barcode scanned
                picam.barcode_queue.get_nowait()
            
            
        time.sleep(1)

def gotmatch(caminput):
    lcd=LCD.lcd()
    db.getallbooks()
    db.getallprofile()
    global profileadm
    profileadm=""
    profileadm=db.matchprofile(caminput)
    print(profileadm)
    if profileadm!="":
        lcd.lcd_clear()
        lcd.lcd_display_string("1-Collect Books",1)
        lcd.lcd_display_string("2-Return Books",2)
        while True:
            if currentkey== 1:
                collectbooks()
                break
            elif currentkey ==2:
                returnbooks()
                break
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("No Account",1)
        lcd.lcd_display_string("Found",2)


def collectbooks():
    lcd=LCD.lcd()
    global profileadm
    gotfine = 0
    print("going in check fine")
    gotfine = db.checkfines(profileadm)
    print(gotfine)
    print(type(gotfine))
    if gotfine!=0:
        lcd.lcd_clear()
        lcd.lcd_display_string("Pls Tap Card to",1)
        lcd.lcd_display_string("pay $"+str(gotfine),2)
        while True:
            #check if got sufficient balance
            balance=rfid.readmoney()
            balance=float(balance)
            if balance<gotfine:
                continue
            #set money from RFID
            rfid.setmoney(str(balance-gotfine))
            rfid.readmoney()
            #Reset fine in firebase
            db.updatefine(profileadm,0)
            lcd.lcd_clear()
            lcd.lcd_display_string("Fine Deducted!",1)
            time.sleep(3)
            break
    #if no fine proceed here
    rharr=rh.get_rh()
    rhavg=rh.calcavg(rharr)
    if rh.is_too_wet(rhavg,80):
        led.set_output(0,1)
        buzzer.init()
        buzzer.beep(0.125,0.125,12)
        led.set_output(0,0)
        print("too wet")
    else:
        print("not too wet")
    # Motor func below      
    sm.servo_motor_open_close()
    buzzer.init()
    buzzer.beep(1.5,1.5,1)
    # Update Firebase Below
    db.collectedloan(profileadm)
    # Return to main menu func
    lcd.lcd_clear()
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)
        

    

def returnbooks():
    lcd=LCD.lcd()
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan Book",1)
    lcd.lcd_display_string("0 to end",2)
    while currentkey!=0:
        #if a barcode has been scanned
        if not picam.barcode_queue.empty():
            caminput=picam.barcode_queue.get()
            print(caminput)
            #check humidity

            #Check firebase for return date
            
            #if return late add fine
            
            #tag late fine amount

            #reset book loan state

            #show confirmation message
       



if __name__ == '__main__':
    main()

#Added thread start for auto reservation removal