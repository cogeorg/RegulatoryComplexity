from flask import Flask
from flask import request, jsonify, redirect, url_for,flash,  render_template, request, session, abort
from helper_functions import *
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, current_user,login_required, logout_user

import os
import json
import csv
import pandas

app = Flask(__name__)
app.secret_key = os.urandom(12)


mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'regulatorycomplexity@gmail.com'
app.config['MAIL_PASSWORD'] = 'baseliii'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


# Define paths
# Local:
#path = 'apps/words/'
# Pythonanywhere
path = 'RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/'

# pre-classified data
# Local:
#pathProt = '/home/sabine/Dokumente/Git/RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list'
# Pythonanywhere:
pathProt = 'RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list'

# Create the engine to use users.db
# Local:
#engine = create_engine('sqlite:///' + path + 'static/users/users.db', echo=True)
# Pythonanywhere
engine = create_engine('sqlite:////home/RegulatoryComplexity/' + path + 'static/users/users.db', echo=True)

# Initialize the Mail object with the app
mail=Mail(app)

# Create a LoginManager()
login_manager = LoginManager()
# Intialize the login_manager with the app
login_manager.init_app(app)


#Home route
@app.route('/')
def home():
    return render_template('login.html')    #Go to the login page

#login route, method POST
@app.route('/login', methods=['POST'])
def do_admin_login():
    error = None                                #initialize error
    USERNAME = str(request.form['username'])    #Request username from login.html
    PASSWORD = str(request.form['password'])    #Request password from login.html
    our_user = user_loader(USERNAME)            #user_loader function with USERNAME
    if not our_user:                            #if the our_user is not found
        error = "Username not found"            #error
    elif our_user.password == PASSWORD:         #if password requested same than our_user.password
        login_user(our_user, remember=True)     #login_user (from LoginManager)
        return  render_template("index.html", username = our_user.username ) # Everything correct! Go to index and send username
    else:
            error = "Incorrect Password"        #if password requested not the same
    return render_template("login.html", error = error) # Go to login winth error message

#register route, method post
@app.route('/register', methods=['POST'])
def do_admin_signin():
    error = None
    USERNAME = str(request.form['username'])   #Request username from login.html
    PASSWORD = str(request.form['password'])   #Request password from login.html
    EMAIl = str(request.form['email'])         #Request email from login.html
    AFILIATION =  str(request.form['afiliation']) #Request afiliation from login.html
    CONFIRMPASS = str(request.form['password2'])  #Request password from login.html
    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(username=USERNAME).first()    #Get the user with the email
    file = path + "output/" + USERNAME.strip() + ".csv" #Name of the file to be created

    if our_user:                                #if our_user different than null
        error = "Username already exists"       #Username already exists
        return render_template("login.html", error = error) #Go to login with error
    elif PASSWORD == "" or EMAIl =="" or AFILIATION =="" or CONFIRMPASS== "": #if a field is null
        error = "Please fill all the fields"    # error, please fill all the fields
        render_template("login.html", error = error)    #Go to login with error
    elif PASSWORD != CONFIRMPASS:               # if password different than confirm password
        error = "Passwords do not match"
        render_template("login.html", error = error)   #Go to login with error
    elif not our_user:                          # if not user, create user
        user = User(USERNAME,PASSWORD,EMAIl, AFILIATION, True)  # Add to the database
        s.add(user)
        s.commit()
        with open(file, "w") as f:              #Create a csv file for the list of words
            pass
    return render_template("login.html", error = error)


#recover route, method POST
@app.route('/recover', methods=['POST'])
def do_recover_password():
    error = "Password sent"                     # Called error but it is a message
    EMAIL= str(request.form['email'])           # Request email from login.html
    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(email=EMAIL).first() #Get the user with the email
    if our_user:
        # Message attributes
        msg = Message(sender="RegulatoryComplexity@gmail.com")
        msg.add_recipient(EMAIL)
        msg.subject = "Password recovery"
        msg.body = "hello, %s" % our_user.username + " your password is %s" % our_user.password
        mail.send(msg)
    else:
        error = "Email not found"               # error email not found
    return render_template("login.html", error = error)     # Go to login


@app.route("/logout")
@login_required                                 # Access to logout just if the user is logged
def logout():
    logout_user()                               #log_out user
    return render_template("login.html")



@app.route("/index")                            # Access to index just if the user is logged
@login_required
def index():
    user_name = current_user.username           # Get the current user
    return render_template('index.html', username = user_name )



@app.route("/instructions")
@login_required
def instructions():
    return render_template('instructions.html')


@app.route("/words")
@login_required
def words():
    user_name = current_user.username           # Get the current user
    # own data
    file = path + "output/" + user_name.strip() + ".csv"   # File name for the current user
    data = pandas.read_csv(file, names=['word', 'type'])    # Open file
    words, types, remove= delete_white(data.word.tolist(), data.type.tolist())  #Delete white words
    colors = operand_to_color(types)         #Get the color for each operand

    return render_template('words.html', words = words ,types = types, colors = colors) #Send words and types to the html


@app.route("/_words2html",  methods=['POST'])
@login_required
def words2html():
    user_name = current_user.username           # Get the current user
    # own data
    file = path + "output/" + user_name.strip() + ".csv"   # File name for the current user
    data = pandas.read_csv(file, names=['word', 'type'])    # Open file
    words, types, remove= delete_white(data.word.tolist(), data.type.tolist())  #Delete white words
    colors = operand_to_color(types)         #Get the color for each operand

    preWords = []
    preClass = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            wordClass = filename.strip('.txt')
            wordClass = wordClass.split('_')[0]
            with open(pathProt + '/' + filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    line = line.strip(',')
                    line = line.strip('.')
                    line = line.strip('`')
                    preWords.append(line)
                    preClass.append(wordClass)

    return jsonify(words = words ,types = types, preWords = preWords, preClass = preClass)



#array2python function to get the list of words classified from the visualizer
# and export it to a csv file
@app.route('/_array2python', methods=['POST'])
@login_required
def array2python():
    user_name = request.json['user_name']                #Get user_name from parameters
    wordlist = request.json['wordList']                       #Get wordList from parameters (new words and colors)
    new_words, new_colors = [],[]                       #Initialize new_words and new_colors
    file = path + "output/" + user_name.strip()  + ".csv"  #File of the user

    data = pandas.read_csv(file, names=['word', 'type'])
    classified_words = data.word.tolist()               #Convert the data.word to list
    type_words =data.type.tolist()                      #Convert the data.type to list
    colors_words = operand_to_color(type_words)         #Get the color for each operand
    dict_words = dict(zip(classified_words, colors_words))  #Make a dictionary for words and colors from csv

    #Format the wordlist
    for element in wordlist:
            word = element.split("_")[0]                #Split and get the first element(word)
            word = word.strip()
            word = word.replace('  ',' ')               #To get the original string
            word = word.lower()                         #To lower in all the cases
            word = check_punctuation(word)
            dict_words[word] = element.split("_")[1]    #Second element is the color
            new_words.append(word)                      #The list of new words
            new_colors.append(element.split("_")[1])    #The list of new colors
    classified_words = dict_words.keys()                #Split dictionary in lists
    colors_words = dict_words.values()
    classified_words, colors_words, remove_words = delete_white(classified_words, colors_words)
    # classified_words, colors_words = sort_list_len(classified_words, colors_words)
    # Export to the csv file
    with open(file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zip(classified_words, color_to_operand(colors_words)))
    # Return Lists to html
    return jsonify(words = classified_words, colors = colors_words,
                   remove=remove_words, new_words = new_words, new_colors = new_colors)



#User_loader function to load user from the database
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(username=user_id).first()
    return our_user

from titles import *
