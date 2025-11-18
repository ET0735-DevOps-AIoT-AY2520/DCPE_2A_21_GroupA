import firebase_admin
from firebase_admin import credentials, firestore

# Load service account key file
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
    
    for doc in books:
        print(f"\nDocument ID: {doc.id}")
        data = doc.to_dict()
        print("Data:", data["id"])
    

    
