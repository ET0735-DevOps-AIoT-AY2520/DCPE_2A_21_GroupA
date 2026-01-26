import db as db
import datetime

def test_matchprofiles():
    db.getallbooks()
    db.getallprofile()
    
    assert(db.matchprofile("P2426082")=="P2426082")
    assert(db.matchprofile("asdnaios@3")=="")

def test_find_reserved_books():
    db.getallbooks()
    result=""
    ans=db.find_reserved_books("P2426082")
    for a in ans:
        if a["title"]=="pytest_book":
            result=a["title"]
    assert(result=="pytest_book")

def test_checkfines():
    db.getallprofile()
    fines=""
    fines=db.checkfines("P2426083")
    assert(fines==0)

def test_calculatefine():
    result=db.calculatefine(
    [
        {"extended":True,"date":"2025-12-06"},
        {"extended":False,"date":"2025-12-03"},
        {"extended":True,"date":"2025-11-26"},
        {"extended":False,"date":"2025-12-16"},
    ],
        datetime.datetime.strptime("2025-12-23", "%Y-%m-%d").date()
    )
    assert(result==0.6)

#2+2=4*0.15=0.6