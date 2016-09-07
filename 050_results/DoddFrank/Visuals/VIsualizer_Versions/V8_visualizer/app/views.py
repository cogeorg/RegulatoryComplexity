from flask import request, jsonify, redirect, url_for,flash,  render_template, request, session, abort
from helper_functions import *
from app import app
import json
import csv
import pandas
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask_mail import Mail, Message


engine = create_engine('sqlite:///app/static/users/users.db', echo=True)
mail=Mail(app)


@app.route('/')
def home(*args):
    if not session.get('logged_in'):
        if len(args)>0:
            return render_template('login.html', error = args[0])
        else:
            return render_template('login.html')
    else:
        if len(args)>0:
         return render_template('index.html', username = args[0])
        else:
         return render_template('index.html')


@app.route("/instructions", methods=['POST'])
def instructions():
    username = str(request.form["username"])
    return render_template('instructions.html')


@app.route("/words", methods=['POST'])
def words():
    user_name = str(request.form["username"])
    file = "app/output/" + user_name.strip() + ".csv"
    data = pandas.read_csv(file, names=['word', 'type'])
    words, types, remove= delete_white(data.word.tolist(), data.type.tolist())
    return render_template('words.html', words = words ,types = types)


@app.route("/index")
def index():
    if  session.get('logged_in'):
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():

    USERNAME = str(request.form['username'])
    PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(username=USERNAME).first()
    if not our_user:
        error = "Username not found"
    elif our_user.password == PASSWORD:
        session['logged_in'] = True
        error = USERNAME
    else:
            error = "Incorrect Password"
    return home(error)


@app.route('/register', methods=['POST'])
def do_admin_signin():
    error = ""
    USERNAME = str(request.form['username'])
    PASSWORD = str(request.form['password'])
    EMAIl = str(request.form['email'])
    AFILIATION =  str(request.form['afiliation'])
    CONFIRMPASS = str(request.form['password2'])
    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(username=USERNAME).first()
    file = "app/output/" + USERNAME.strip() + ".csv"
    with open(file, "w") as f:
       pass
    if our_user:
        error = "Username already exists"
    elif PASSWORD == "" or EMAIl =="" or AFILIATION =="" or CONFIRMPASS== "":
        error = "Please fill all the fields"
    elif PASSWORD != CONFIRMPASS:
        error = "Passwords do not match"
    elif not our_user:
        user = User(USERNAME,PASSWORD,EMAIl, AFILIATION)
        s.add(user)
        s.commit()
    return home(error)


@app.route('/recover', methods=['POST'])
def do_recover_password():
    error = "Password sent"
    EMAIL= str(request.form['email'])
    Session = sessionmaker(bind=engine)
    s = Session()
    our_user = s.query(User).filter_by(email=EMAIL).first()
    if our_user:
        msg = Message(sender="alij.limon@gmail.com")
        msg.add_recipient(EMAIL)
        msg.subject = "Password recovery"
        msg.body = "hello, %s" % our_user.username + " your password is %s" % our_user.password
        mail.send(msg)
    else:
        error = "Email not found"
    return home(error)


@app.route("/logout", methods=['POST'])
def logout():
    username = str(request.form["username"])
    session['logged_in'] = False
    error = "see you soon " + username
    return home(error)



@app.route('/_array2python')
def array2python():
    params = json.loads(request.args.get('params'))
    user_name = params['user_name']
    wordlist = params['wordList']
    new_words, new_colors = [],[]
    file = "app/output/" + user_name.strip()  + ".csv"
    data = pandas.read_csv(file, names=['word', 'type'])
    classified_words = data.word.tolist()
    type_words =data.type.tolist()
    colors_words = operand_to_color(type_words)
    dict_words = dict(zip(classified_words, colors_words))
    for element in wordlist:
            word = element.split("_")[0]
            word = word.strip()
            word = word.replace('  ',' ')
            word = word.lower()
            word = check_punctuation(word)
            dict_words[word] = element.split("_")[1]
            new_words.append(word)
            new_colors.append(element.split("_")[1])
    classified_words = dict_words.keys()
    colors_words = dict_words.values()
    classified_words, colors_words, remove_words = delete_white(classified_words, colors_words)
    # classified_words, colors_words = sort_list_len(classified_words, colors_words)
    with open(file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zip(classified_words, color_to_operand(colors_words)))
    return jsonify(words = classified_words, colors = colors_words,
                   remove=remove_words, new_words = new_words, new_colors = new_colors)

