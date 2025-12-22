import firebase_admin
from firebase_admin import credentials, firestore
import threading as thread
import time
import datetime
# Load your service account key file
cred = credentials.Certificate("/home/pi/ET0735/DCPE_2A_21_GroupA/serviceAccoutKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

print("Reading all documents from 'books' collection...")

# Read all documents in the 'books' collection
def getallbooks():
    global books
    books = list(db.collection("books").stream())

    # Loop through documents
    '''
    for doc in books:
        print(f"\nDocument ID: {doc.id}")
        data = doc.to_dict()
        print("Data:", data["id"])
    '''

def getallprofile():
    global profiles
    profiles = list(db.collection("profile").stream())

    # Loop through documents
    '''
    for profile in profiles:
        print(f"\nDocument ID: {profile.id}")
        data = profile.to_dict()
        print("Data:", data["adm"])
    '''

def matchprofile(input):
    global profiles
    global books
    for profile in profiles:
        
        if profile.to_dict()["adm"]==str(input):
            print(profile.to_dict()["adm"])
            return str(profile.to_dict()["adm"])
           
    return ""                        

def find_reserved_books(input):
    global books
    result=[]
    for book in books:
        a=book.to_dict()
        if a["loanadm"]==str(input) and a["reserved"]==True:
            print(a["title"])
            print(a["location"])
            result.append(a)
    
    return result

def checkfines(input):
    for profile in profiles:
        a=profile.to_dict()
        if a["adm"]==input:
            return float(a["fine"])
    return 0

def updatefine(target,data):
    global profiles
    id=""
    for profile in profiles:
        if profile.to_dict()["adm"]==target:
            id=profile.id
    if id!="":
        db.collection("profile").document(id).update({"fine":data})


def reservationTimeout():
    global books
    global profiles
    while True:
        #force a database update
        getallbooks()
        getallprofile()
        #iterate thru every profile
        for item in profiles:
            item=item.to_dict() #convert snapshot object to dict
            reservedarr=[]
            reservedarr=find_reserved_books(item["adm"])
            if len(reservedarr)>0: #if this account has any reserved book
                for book in reservedarr: #iterate thru all reserved books in this account
                    # documentation for datetime import: https://docs.python.org/3/library/datetime.html
                    reserved_date = datetime.datetime.strptime(book["date"], "%Y-%m-%d").date()
                    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=5)).date()

                    if reserved_date < cutoff_date:
                        remreserve(book["id"])

                #find any books reserved
            
        time.sleep(10*60)
    
def remreserve(bookid):
    global books
    print("remove the reservation here")
    print(bookid)
reservationTimeout()

#changed date comparison strat to use datetime and timedelta, call remreserve func to rem 5day old reservations