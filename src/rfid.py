from hal import hal_rfid_reader as rfid

def main():
    print("testing RFID")
    reader=rfid.init()
    temp=reader.read_id()
    print(str(temp))


if __name__ == "__main__":
    main()

# initial rfid read testing
