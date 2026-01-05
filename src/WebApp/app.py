
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
from flask import render_template
import db
app=Flask(__name__)

def getdbdata():
    global books
    global profiles
    db.getallbooks()
    db.getallprofile()
    books=[]
    profiles=[]
    for book in db.books:
        books.append(book.to_dict())
    for profile in db.profiles:
        profiles.append(profile.to_dict())
    


@app.route('/')
def index():
    getdbdata()
    return render_template("index.html",books=books,profiles=profiles)

@app.route('/booksearch')
def booksearch():
    return render_template("booksearch.html")

@app.route('/usersearch')
def usersearch():
    return render_template("usersearch.html")


@app.route('/logs')
def logs():
    return render_template("logs.html")


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Added calling of db for data