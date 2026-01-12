import firebase_admin
from firebase_admin import credentials, firestore
import threading as thread
import time
import datetime
import logs
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
    logs.newlog(1,"Reading from DB Books")
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
    logs.newlog(1,"Reading from DB profiles")
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
    logs.newlog(0,"Found "+str(len(result))+"Reserved Books")
    return result

def checkfines(input):
    logs.newlog(0,"Checking Fines")
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
        logs.newlog(2,"Updated "+id+"fine to "+str(data))

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
                logs.newlog(2,"Updated"+str(adm)+" books: "+str(book.to_dict()["title"])+" to loaned")

def checkprofile(adm):
    getallprofile()
    global profiles
    for profile in profiles:
        a=profile.to_dict()
        if a["adm"]==adm:
            return a

def checkreturndate(adm,returned):
    global books
    global profiles
    getallbooks()
    getallprofile()
    result=[]
    for i in range(0,len(returned)):
        for book in books:
            if book.to_dict()["onloan"]==True and book.to_dict()["loanadm"]==adm and book.to_dict()["location"]==locationdict[setlocation] and book.to_dict()["id"]==returned[i]:
                result.append(book.to_dict())
    print(result)
    return result

def calculatefine(input,timenow):
    totaldayslate=0
    for book in input:
        reserved_date = datetime.datetime.strptime(book["date"], "%Y-%m-%d").date()
        if book["extended"]==True:
            cutoff=(timenow - datetime.timedelta(days=21))
        else:
            cutoff=(timenow - datetime.timedelta(days=14))
        if reserved_date<cutoff:
            totaldayslate+=(cutoff-reserved_date).days
    totalfine=totaldayslate*0.15
    print(totalfine)
    return totalfine

def remloan(scanned):
    getallbooks()
    global books
    for i in range(0,len(scanned)):
        for book in books:
            a=book.to_dict()
            if a["id"]==scanned[i]:
                db.collection("books").document(book.id).update({
                    "date":"",
                    "extended":False,
                    "loanadm":"",
                    "onloan":False,
                    "reserved":False,})


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

def updbookweb(id,date,title,location,loanadm,reserved,onloan,delflag):
    getallbooks()
    print(delflag)
    print(type(delflag))
    global books
    for book in books:
        if book.to_dict()['id']==id:
            if delflag=="1":
                db.collection("books").document(book.id).delete()
            else:
                print("updating book")
                if reserved=="true":
                    reserved=True
                else:
                    reserved=False
                if onloan=="true":
                    onloan=True
                else:
                    onloan=False
                db.collection("books").document(book.id).update({
                    "date":date,
                    "loanadm":loanadm,
                    "onloan":onloan,
                    "reserved":reserved,
                    "title":title,
                    "location":location,})

def upduserweb(id,delete,fine):
    getallprofile()
    global profiles
    for profile in profiles:
        if profile.to_dict()["adm"]==id:
            if delete=="1":
                db.collection("profile").document(profile.id).delete()
            else:
                db.collection("profile").document(profile.id).update(
                    {
                        "fine":float(fine)
                    }
                )

def createnewbook(id,title,locationcode):
    db.collection("books").add({
        "date":"",
        "extended":False,
        "loanadm":"",
        "onloan":False,
        "reserved":False,
        "id":id,
        "title":title,
        "location":locationdict[locationcode],
    })
                



