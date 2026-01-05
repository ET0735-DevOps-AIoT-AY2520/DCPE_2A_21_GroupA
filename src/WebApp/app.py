from flask import Flask
from flask import render_template
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/booksearch')
def booksearch():
    return render_template("booksearch.html")

@app.route('/usersearch')
def usersearch():
    return "This is user search"


@app.route('/logs')
def logs():
    return "This is logs"


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0") #0.0.0.0 accessible from all IP

#Added template for booksearch html and return js to index.html