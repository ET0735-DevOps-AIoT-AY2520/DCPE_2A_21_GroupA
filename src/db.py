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

#location details:
locationdict={
    1:"Woodlands Regional",
    2:"Sembawang Library",
}

setlocation = 1

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
        #return books reserved by this user specifically at this location
        if a["loanadm"]==str(input) and a["reserved"]==True and a["location"]==locationdict[setlocation]:
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

def collectedloan(adm):
    getallbooks()
    global books
    global profiles
    reserved=find_reserved_books(adm)
    for i in range(0,len(reserved)):
        for book in books:
            if book.to_dict()["id"]==reserved[i]["id"]:
                print("updated"+book.to_dict()["title"])
                db.collection("books").document(book.id).update({
                    "onloan":True,
                    "reserved":False,
                    "date":str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
                })

def checkreturndate(adm):
    global books
    global profiles
    getallbooks()
    getallprofile()
    dates=[]
    for book in books:
        if book.to_dict()["onloan"]==True and book.to_dict()["loanadm"]==adm:
            dates.append(book.to_dict()["date"])
    print(dates)
    return dates



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
            
        time.sleep(1*60)
    
def remreserve(bookid):
    global books
    
    for book in books:
        if book.to_dict()["id"]==bookid:
            print('removed:'+book.to_dict()["title"])
            db.collection("books").document(book.id).update({"date":"","extended":False,"loanadm":"","onloan":False,"reserved":False,})


checkreturndate("P2426082")