from flask import request, jsonify, redirect, url_for,flash,  render_template, request, session, abort
from flask_login import current_user
from app import app

import os

cwd = os.getcwd()




@app.route('/title_1')
def title_1_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_1.html')

@app.route('/title_2')
def title_2_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_2.html')

@app.route('/title_3')
def title_3_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_3.html')

@app.route('/title_4')
def title_4_Y():
    username = current_user.username
    return render_template("/output/" + username + '/title_4.html')

@app.route('/title_5')
def title_5_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_5.html')

@app.route('/title_6')
def title_6_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_6.html')

@app.route('/title_7')
def title_7_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_7.html')

@app.route('/title_8')
def title_8_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_8.html')

@app.route('/title_9')
def title_9_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_9.html')

@app.route('/title_10')
def title_10_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_10.html')

@app.route('/title_11')
def title_11_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_11.html')

@app.route('/title_12')
def title_12_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_12.html')

@app.route('/title_13')
def title_13_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_13.html')

@app.route('/title_14')
def title_14_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_14.html')

@app.route('/title_15')
def title_15_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_15.html')

@app.route('/title_16')
def title_16_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_16.html')





@app.route('/title_1_O')
def title_1():
    return render_template('Original/title_1.html')

@app.route('/title_2_O')
def title_2():
    return render_template('Original/title_2.html')

@app.route('/title_3_O')
def title_3():
    return render_template('Original/title_3.html')

@app.route('/title_4_O')
def title_4():
    return render_template('Original/title_4.html')

@app.route('/title_5_O')
def title_5():
    return render_template('Original/title_5.html')

@app.route('/title_6_O')
def title_6():
    return render_template('Original/title_6.html')

@app.route('/title_7_O')
def title_7():
    return render_template('Original/title_7.html')

@app.route('/title_8_O')
def title_8():
    return render_template('Original/title_8.html')

@app.route('/title_9_O')
def title_9():
    return render_template('Original/title_9.html')

@app.route('/title_10_O')
def title_10():
    return render_template('Original/title_10.html')

@app.route('/title_11_O')
def title_11():
    return render_template('Original/title_11.html')

@app.route('/title_12_O')
def title_12():
    return render_template('Original/title_12.html')

@app.route('/title_13_O')
def title_13():
    return render_template('Original/title_13.html')

@app.route('/title_14_O')
def title_14():
    return render_template('Original/title_14.html')

@app.route('/title_15_O')
def title_15():
    return render_template('Original/title_15.html')

@app.route('/title_16_O')
def title_16():
    return render_template('Original/title_16.html')
