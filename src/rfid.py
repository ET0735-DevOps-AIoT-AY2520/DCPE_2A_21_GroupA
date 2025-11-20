from hal import hal_rfid_reader as rfid

def setup():
    print("testing RFID")
    global reader
    reader=rfid.init()
    
    reader.write("12345")
    #data is already in string
    

def readmoney():
    global reader
    #from hal file temp is a tuple
    #https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
    #get the second part of the tuple which contains the data, remove empty space and reassign
    data=reader.read()
    balance=data[1].strip()
    print(balance)
    return balance

def setmoney():
    print("")



# bugfix, removed unneccasry read code in setup and made reader in readmoney access global
