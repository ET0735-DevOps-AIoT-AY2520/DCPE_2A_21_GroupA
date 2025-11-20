from hal import hal_rfid_reader as rfid

def main():
    print("testing RFID")
    reader=rfid.init()
    reader.write("12345")
    temp=reader.read()
    #from hal file temp is a tuple
    #https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
    #get the second part of the tuple which contains the data, remove empty space and reassign
    temp=temp[1].strip()
    #data is already in string
    print(temp)


if __name__ == "__main__":
    main()

# Added Basic writing using rfid
