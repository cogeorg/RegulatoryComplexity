from flask import Flask
from flask import render_template

app = Flask(__name__)

#Home route
@app.route('/')
def welcome():
    return render_template('welcome.html')    #Go to the welcome page

@app.route('/about')
def about():
    return render_template('about.html')    #Go to the about us page
