from flask import request, jsonify, redirect, url_for,flash,  render_template, request, session, abort
from flask_login import current_user, login_required
from views import app

import os

cwd = os.getcwd()


@app.route('/title_0')
@login_required
def title_0_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_0.html')

@app.route('/title_1')
@login_required
def title_1_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_1.html')

@app.route('/title_2')
@login_required
def title_2_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_2.html')

@app.route('/title_3')
@login_required
def title_3_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_3.html')

@app.route('/title_4')
@login_required
def title_4_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_4.html')

@app.route('/title_5')
@login_required
def title_5_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_5.html')

@app.route('/title_6')
@login_required
def title_6_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_6.html')

@app.route('/title_7')
@login_required
def title_7_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_7.html')

@app.route('/title_8')
@login_required
def title_8_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_8.html')

@app.route('/title_9')
@login_required
def title_9_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_9.html')

@app.route('/title_10')
@login_required
def title_10_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_10.html')

@app.route('/title_11')
@login_required
def title_11_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_11.html')

@app.route('/title_12')
@login_required
def title_12_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_12.html')

@app.route('/title_13')
@login_required
def title_13_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_13.html')

@app.route('/title_14')
@login_required
def title_14_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_14.html')

@app.route('/title_15')
@login_required
def title_15_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_15.html')

@app.route('/title_16')
@login_required
def title_16_Y():
    username = current_user.username
    return render_template("output/" + username + '/title_16.html')



@app.route('/title_0_O')
def title_0():
    return render_template('Original/title_0.html')

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
