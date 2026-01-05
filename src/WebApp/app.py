from flask import Flask
from flask import render_template
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/booksearch')
def booksearch():
    return "This is book search"

@app.route('/usersearch')
def usersearch():
    return "This is user search"


@app.route('/logs')
def usersearch():
    return "This is user search"


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Added structure for all rotues