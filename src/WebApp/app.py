
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
from flask import render_template
import db
app=Flask(__name__)

def getdbdata():
    db.getallbooks()
    db.getallprofile()
    location=db.locationdict[db.setlocation]
    books=[]
    profiles=[]
    for book in db.books:
        books.append(book.to_dict())
    for profile in db.profiles:
        profiles.append(profile.to_dict())
    return [books,profiles,location]
    


@app.route('/')
def index():
    [books,profiles,location]=getdbdata()
    return render_template("index.html",books=books,profiles=profiles,location=location)

@app.route('/booksearch')
def booksearch():
    [books,profiles,location]=getdbdata()
    return render_template("booksearch.html",books=books,profiles=profiles,location=location)

@app.route('/usersearch')
def usersearch():
    [books,profiles,location]=getdbdata()
    return render_template("usersearch.html",books=books,profiles=profiles,location=location)


@app.route('/logs')
def logs():
    return render_template("logs.html")


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Bug Fix, added missing search button