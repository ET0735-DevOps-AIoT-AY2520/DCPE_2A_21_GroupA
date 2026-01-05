
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
from flask import render_template
from flask import request, redirect
import db
app=Flask(__name__)

def getdbdata():
    #call db.py to get books and profile
    db.getallbooks()
    db.getallprofile()
    #take all the infomation from the global var in db.py
    location=db.locationdict[db.setlocation]
    books=[]
    profiles=[]
    #convert books and profiles to dict format first
    for book in db.books:
        books.append(book.to_dict())
    for profile in db.profiles:
        profiles.append(profile.to_dict())
        #send the result back
    return [books,profiles,location]
    


@app.route('/')
def index():
    #get database data and send it to main menu
    [books,profiles,location]=getdbdata()
    return render_template("index.html",books=books,profiles=profiles,location=location)

@app.route('/booksearch')
def booksearch():
    #get database data and send it to book search 
    [books,profiles,location]=getdbdata()
    return render_template("booksearch.html",books=books,profiles=profiles,location=location)

@app.route('/usersearch')
def usersearch():
    #get database data and send it to user search
    [books,profiles,location]=getdbdata()
    return render_template("usersearch.html",books=books,profiles=profiles,location=location)

#https://www.geeksforgeeks.org/html/retrieving-html-from-data-using-flask/
@app.route('/booksearch/edit',methods=["POST"])
def bookedit():
    #get all the data from the body
    if request.method == "POST":
        id = request.form.get("id")
        title = request.form.get("title")
        location = request.form.get("location")
        loanadm = request.form.get("loanadm")
        reserved = request.form.get("reserved")
        loaned = request.form.get("onloan")
        date= request.form.get("date")
        #convert data into JSOn and send it to the next HTML for editing
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

#This function for editing user
@app.route('/usersearch/edit',methods=["POST"])
def useredit():
    if request.method == "POST":
        #get the id and fine from body of page 
        id = request.form.get("id")
        fine = request.form.get("fine") 
        #convert to JSON and send it to useredit
        jsonuser={
            "id":id,
            "fine":fine,
        }
    return render_template("useredit.html",users=jsonuser)

@app.route('/booksearch/upd',methods=["POST"])
def getbookupdate():
    #get all data from body of html
    id = request.form.get("id")
    title = request.form.get("title")
    location = request.form.get("location")
    loanadm = request.form.get("loanadm")
    reserved = request.form.get("reserved")
    onloan = request.form.get("onloan")
    date= request.form.get("date")
    #temporary confirmation of data downloading
    print(id)
    print(date)
    print(title)
    print(location)
    print(loanadm)
    print(reserved)
    print(onloan)
    #immediately send the user back to main screen after data acquired
    return redirect('/')

@app.route('/usersearch/upd',methods=["POST"])
def getuserupdate():
    #download all data from body of html
    id = request.form.get("id")
    fine = request.form.get("fine")
    delete = request.form.get("del")
    #temporary confirmation of data downloading
    print(delete)
    print(id)
    print(fine)
    #send user back to main menu
    return redirect('/')

@app.route('/logs')
def logs():
    return render_template("logs.html")


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Added delete button for Users