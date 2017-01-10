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
import shutil

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)
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
path = 'apps/sentences/'
# Pythonanywhere
#path = 'RegulatoryComplexity/RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/sentences/'

# Create the engine to use users.db
# Local:
engine = create_engine('sqlite:///' + path + 'static/users/users.db', echo=True)
# Pythonanywhere
#engine = create_engine('sqlite:////home/' + path + 'static/users/users.db', echo=True)


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
    return render_template("login.html", error = error) # Go to login with error message

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

    # txt file for graph tables
    file = path + "output/" + USERNAME.strip() + ".txt" #Name of the file to be created

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
        with open(file, "w") as f:              #Create a txt file for graphs
            pass

        # create folder with own html files
        os.makedirs(path + "templates/output/" + USERNAME.strip())
        copytree(path + 'templates/Original', path + "templates/output/" + USERNAME.strip())

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
    user_name = current_user.username           # Get the current user
    return render_template('instructions.html', username = user_name )


@app.route('/_html2python', methods=['POST'])
@login_required
def html2python():
    user_name = request.json['user_name']                     #Get user_name from parameters
    htmlString = request.json['file']
    titleName = request.json['title']

    head= """<!DOCTYPE html> <html>
        <head>
        </head>
        <body>"""

    tail= """
        </body>
        </html>
        """

    data = head + htmlString + tail
    username = user_name.strip()
    f = open(path + "templates/output/" + username + "/" + titleName + ".html", "w")
    f.write(data)
    f.close()
    return render_template('index.html', username = user_name )


#array2python function to get the list of checked checkboxes and export it to a csv file
@app.route('/_array2python', methods=['POST'])
@login_required
def array2python():
    userName = request.json['userName']
    titleName = request.json['titleName']
    inputIds = request.json['inputIds']
    checks = request.json['checks']

    p = path + "output/" + userName.strip()  + ".txt"
    file = p  #File of the user
    if len(checks) > 0:
        oldFile = []
        newFile = []
        with open(file, "r") as f:
            # if file is not empty, save all old settings
            if os.stat(path).st_size != 0:
                for line in f:
                    split = line.split(',')
                    if len(split) < 2:
                        continue
                    else:
                        for s in range(len(split)):
                            split[s] = split[s].strip()
                        oldFile.append(split)

        for item in oldFile:
            # if old settings dont concern current title, keep them
            if item[0] != titleName:
                newFile.append(item)
            # if they concern current title, overwrite them with new settings
            else:
                for inputId in inputIds:
                    if item[1] == inputId:
                        newFile.append([titleName, inputId, checks[inputIds.index(inputId)]])

        # append all new settings that did not exist before
        for inputId in inputIds:
            newItem = [titleName, inputId, checks[inputIds.index(inputId)]]
            if newItem not in newFile:
                newFile.append(newItem)

        # write into user file
        with open(file, "w") as f:
            for item in newFile:
                string = item[0] + ',' + item [1] + ',' + str(item[2]) + '\n'
                f.write(string)

    return jsonify(userName = userName)

@app.route('/_array2javascript', methods=['POST'])
@login_required
def array2javascript():
    userName = request.json['userName']
    titleName = request.json['titleName']

    p = path + "output/" + userName.strip()  + ".txt"
    file = p  #File of the user
    inputJson = []
    checksJson = []
    # load user file and pass data to javascript
    with open(file, "r") as f:
        for line in f:
            data = line.split(',')
            if data[0] == titleName:
                inputJson.append(data[1])
                checksJson.append(data[2])

    return jsonify(userName = userName, titleName = titleName, inputIds = inputJson, checks = checksJson)


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
