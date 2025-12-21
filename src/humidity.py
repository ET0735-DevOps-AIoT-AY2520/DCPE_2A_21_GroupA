from hal import hal_temp_humidity_sensor as temp_humid_sensor
import time
def is_too_wet(rh,threshold):
    if rh>threshold:
        return True
    else:
        return False
    

def get_rh():
    #humidity sensor is garbage, wait till valid read and return the 5 latest valid
    temp_humid_sensor.init()
    return temp_humid_sensor.read_temp_humidity()




def dht11_tester():
    temp_humid_sensor.init()
    while True:
        time.sleep(1)
        print(get_rh())

dht11_tester()

#added basic humidity read