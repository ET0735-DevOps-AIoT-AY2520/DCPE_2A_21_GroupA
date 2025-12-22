from hal import hal_servo as servo 
import time

def servo_motor_open_close():
    servo.init()

    #Open the lid (rotate the hand to 90 degree) for 2 seconds
    servo.set_servo_position(90)
    time.sleep(2)

    #Close the lid (rotate back to 0 degree)
    servo.set_servo_position(0)
    time.sleep(0.5)
