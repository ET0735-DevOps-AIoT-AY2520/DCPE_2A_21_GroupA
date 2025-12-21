from hal import hal_temp_humidity_sensor as temp_humid_sensor
import time
def is_too_wet(rh,threshold):
    if rh>threshold:
        return True
    else:
        return False
    

def get_rh():
    #humidity sensor is garbage, wait till valid read and return the 5 latest valid
    arr=[]
    temp_humid_sensor.init()
    while True:
        result=temp_humid_sensor.read_temp_humidity()
        if result!= [-100,-100]:
            arr.append(result[1])
        if len(arr)>=5:
            return arr
        time.sleep(0.1)
        

def calcavg(arr):
    total=0
    for item in arr:
        total+=item
    return total/len(arr)


def dht11_tester():
    temp_humid_sensor.init()
    while True:
        time.sleep(1)
        print(calcavg(get_rh()))
        

#added averaging of the humidity for better result