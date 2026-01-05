
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
from flask import render_template
from flask import request, redirect
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

#https://www.geeksforgeeks.org/html/retrieving-html-from-data-using-flask/
@app.route('/booksearch/edit',methods=["POST"])
def bookedit():
    if request.method == "POST":
        id = request.form.get("id")
        title = request.form.get("title")
        location = request.form.get("location")
        loanadm = request.form.get("loanadm")
        reserved = request.form.get("reserved")
        loaned = request.form.get("onloan")
        date= request.form.get("date")
        jsonbook={
            "id":id,
            "title":title,
            "location":location,
            "loanadm":loanadm,
            "reserved":reserved,
            "onloan":loaned,
            "date":date,
        }
    return render_template("bookedit.html",books=jsonbook)

#This function is for
@app.route('/usersearch/edit',methods=["POST"])
def useredit():
    if request.method == "POST":
        id = request.form.get("id")
        fine = request.form.get("fine") 
        jsonuser={
            "id":id,
            "fine":fine,
        }
    return render_template("useredit.html",users=jsonuser)

@app.route('/booksearch/upd',methods=["POST"])
def getbookupdate():
    id = request.form.get("id")
    title = request.form.get("title")
    location = request.form.get("location")
    loanadm = request.form.get("loanadm")
    reserved = request.form.get("reserved")
    onloan = request.form.get("onloan")
    date= request.form.get("date")
    print(id)
    print(date)
    print(title)
    print(location)
    print(loanadm)
    print(reserved)
    print(onloan)
    return redirect('/')

@app.route('/logs')
def logs():
    return render_template("logs.html")


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Added basic page for user fine editing