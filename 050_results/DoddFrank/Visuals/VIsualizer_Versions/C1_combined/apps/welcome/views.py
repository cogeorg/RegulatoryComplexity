from flask import Flask
from flask import render_template

app = Flask(__name__)

#Home route
@app.route('/')
def welcome():
    return render_template('welcome.html')    #Go to the welcome page
