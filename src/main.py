import time
from threading import Thread
import queue
import datetime

import db as db
import picam as picam
import rfid 
import humidity as rh
import servo_motor as sm
import logs 
from WebApp.app import app

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
import nonfunc as mode





#Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    global currentkey
    currentkey=key
    logs.newlog(4,"Keypad Pressed"+ str(currentkey))
    time.sleep(1)
    currentkey="z"
    



def main():
    global currentkey
    currentkey="z"
    logs.newlog(0,"Init LCD")
    lcd = LCD.lcd()
    lcd.lcd_clear()
    logs.newlog(0,"Init RFID")
    rfid.setup()
    logs.newlog(0,"Init LED")
    led.init()
    # Display something on LCD
    logs.newlog(5,"Initial LCD displayed")
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)
    logs.newlog(0,"Init PICam")
    picam.start_scanner()
    # Initialize the HAL keypad driver
    logs.newlog(0,"Init Keypad")
    keypad.init(key_pressed)
    #db autoscan
    logs.newlog(0,"Starting Reservation Timeout Thread")
    remres=Thread(target=db.reservationTimeout)
    remres.start()
    # Start the keypad scanning which will run forever in an infinite while(True) loop in a new Thread "keypad_thread"
    logs.newlog(0,"Start Keypad Thread")
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    mode_thread=Thread(target=mode.monitor)
    mode_thread.start()
    caminput="0"
    while True:
        caminput=picam.barcode_queue.get()
        if caminput != "0": 
            logs.newlog(4,"PiCam Scanned: "+caminput)
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
        logs.newlog(3,"Login Success")
        logs.newlog(5,"Displaying mode selection menu")
        lcd.lcd_clear()
        lcd.lcd_display_string("1-Collect Books",1)
        lcd.lcd_display_string("2-Return Books",2)
        while True:
            if currentkey== 1:
                logs.newlog(0,"Selected Collect book mode")
                collectbooks()
                break
            elif currentkey ==2:
                logs.newlog(0,"Selected return book mode")
                returnbooks()
                break
    else:
        logs.newlog(3,"LOGIN FAILED")
        lcd.lcd_clear()
        lcd.lcd_display_string("No Account",1)
        lcd.lcd_display_string("Found",2)


def collectbooks():
    lcd=LCD.lcd()
    global profileadm
    gotfine = 0
    gotfine = db.checkfines(profileadm)
    if gotfine!=0:
        logs.newlog(5,"Display prompt to pay fine LCD")
        lcd.lcd_clear()
        lcd.lcd_display_string("Pls Tap Card to",1)
        lcd.lcd_display_string("pay $"+str(gotfine),2)
        while True:
            #check if got sufficient balance
            logs.newlog(4,"Reading Money")
            balance=rfid.readmoney()
            balance=float(balance)
            if balance<gotfine:
                logs.newlog(6,"Card insufficient balance")
                continue
            #set money from RFID
            logs.newlog(5,"Updating Money")
            rfid.setmoney(str(balance-gotfine))
            rfid.readmoney()
            #Reset fine in firebase
            db.updatefine(profileadm,0)
            logs.newlog(5,"Displaying confirmation msg")
            lcd.lcd_clear()
            lcd.lcd_display_string("Fine Deducted!",1)
            time.sleep(3)
            break
    #if no fine proceed here
    logs.newlog(4,"Reading Humidity")
    rharr=rh.get_rh()
    rhavg=rh.calcavg(rharr)

    if rh.is_too_wet(rhavg,80):
        logs.newlog(5,"Turn on alert LED")
        led.set_output(0,1)
        buzzer.init()
        buzzer.beep(0.125,0.125,12)
        logs.newlog(5,"Turn on Alert Buzzer")
        led.set_output(0,0)
        logs.newlog(7,"ERROR BOOK IS WET")
        print("too wet")
    else:
        print("not too wet")
    # Motor func below      
    logs.newlog(5,"Turn On motor to dispense books")
    sm.servo_motor_open_close()
    logs.newlog(5,"Turn on Confirmation Buzzer")
    buzzer.init()
    buzzer.beep(1.5,1.5,1)
    # Update Firebase Below
    db.collectedloan(profileadm)
    # Return to main menu func
    logs.newlog(5,"Display LCD Main menu ")
    lcd.lcd_clear()
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)
        

    

def returnbooks():
    lcd=LCD.lcd()
    lcd.lcd_clear()
    logs.newlog(5,"Display LCD prompt to scan books")
    lcd.lcd_display_string("Scan Book",1)
    lcd.lcd_display_string("0 to end",2)
    scanned=[]
    while currentkey!=0:
        #if a barcode has been scanned
        if not picam.barcode_queue.empty():
            caminput=picam.barcode_queue.get()
            logs.newlog(4,"Scanned Book: "+caminput)
            scanned.append(caminput)
            #check humidity
            logs.newlog(4,"Read Humidity of book")
            rharr=rh.get_rh()
            rhavg=rh.calcavg(rharr)
            if rh.is_too_wet(rhavg,80):
                logs.newlog(5,"Turn on Alert Buzzer")
                logs.newlog(5,"Turn on Alert LED")
                led.set_output(0,1)
                buzzer.init()
                buzzer.beep(0.125,0.125,12)
                led.set_output(0,0)
                print("too wet")
            else:
                print("not too wet") 

            #Check firebase for return date
            returnedbooks=db.checkreturndate(profileadm,scanned)
            ans=db.calculatefine(returnedbooks,datetime.datetime.now().date())
            
            #if return late add fine
            if ans !=0:
                currentfine=db.checkprofile(profileadm)["fine"]
                db.updatefine(profileadm,ans+currentfine)

            #reset book loan state
            db.remloan(scanned)
            #show confirmation message
            logs.newlog(5,"Display return books confirm msg LCD")
            lcd.lcd_clear()
            lcd.lcd_display_string("Returned Books!",1)
            time.sleep(1.5)
            logs.newlog(5,"Display Prompt LCD to Scan books")
            lcd.lcd_clear()
            lcd.lcd_display_string("Scan Book",1)
            lcd.lcd_display_string("0 to end",2)
    logs.newlog(5,"Display main menu LCD")
    lcd.lcd_clear()
    lcd.lcd_display_string("Please Scan", 1)
    lcd.lcd_display_string("Your Card", 2)



if __name__ == '__main__':
    t = Thread(target=main, daemon=True)
    t.start()

    # start flask (blocks here)
    app.run(host="0.0.0.0", port=5000, debug=False)

#Added return to main menu REQ-29