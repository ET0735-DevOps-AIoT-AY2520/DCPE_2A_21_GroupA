import db as db

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