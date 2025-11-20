from hal import hal_rfid_reader as rfid

def setup():
    print("testing RFID")
    global reader
    reader=rfid.init()
    reader.write("12345")
    temp=reader.read()
    
    temp=temp[1].strip()
    #data is already in string
    print(temp)

def readmoney():
    #from hal file temp is a tuple
    #https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
    #get the second part of the tuple which contains the data, remove empty space and reassign
    data=reader.read()
    balance=data[1].strip()
    return balance


# Moved read to seperate func, removed main and replaced with setup func
