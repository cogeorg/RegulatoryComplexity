#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:10:43 2019

@author: jane
"""
from flask import render_template, flash, redirect, request, url_for, send_file, session
from flask_login import current_user, login_user
from app.models import User, Submission, CorrectAnswer
from app import app, db
from app.forms import LoginForm, RegistrationForm, RulesForm, SubmissionForm, PracticeForm
from flask_login import login_required, logout_user
from werkzeug.urls import url_parse
import csv
import pandas as pd  
import numpy as np
from datetime import datetime

@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accept_rules'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('accept_rules')
        return redirect(url_for('accept_rules'))
    return render_template('login.html', title = "Sign in", form = form)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('accept_rules'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email=form.email.data, student_id = form.student_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now df registered user!')
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form=form)

@app.route('/accept_rules', methods=["GET", "POST"])
def accept_rules():
    if not current_user.is_authenticated:
        return redirect(url_for("register"))
    form = RulesForm()
    if form.validate_on_submit():
        return redirect(url_for("experiment"))
    return render_template("accept_rules.html", title = "Rules", form=form)


@app.route('/return-excel/')
def return_excel():
    name = 'excel_template.xlsx'
    response = send_file('./static/excel_template.xlsx', as_attachment=True)
    # response.headers["x-filename"] = name
    # response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    # response.headers["Content-Disposition"] = "attachment; filename=" + name

    return response

@app.route("/rules/")
def rules():
    return render_template("rules.html")

@app.route('/experiment', methods=["GET", "POST"])
@app.route('/experiment/<int:n_reg>', methods=["GET", "POST"])
@login_required
def experiment(n_reg=1, Score=0):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user_id = current_user.id
    correctanswer = CorrectAnswer.query.filter_by(id=n_reg).first()
    correctanswer = correctanswer.correctanswer
    user_experiments = []
    for line in open("./app/static/users/user_" + str(user_id) + "_experiments.csv"):
        user_experiments.append(line.strip("\n"))

    df = pd.read_csv("./app/static/table_template.csv") 
    df.to_html("./app/static/table.htm", na_rep="", index=False, index_names=False, col_space=60)
    df.style.set_properties(**{'text-align': 'right'})
    table = df.to_html()

    form = SubmissionForm()
    if n_reg == 1:
        form = PracticeForm()
    else: 
        form = SubmissionForm()
 
    if form.validate_on_submit():
        submission = Submission(answer = form.answer.data, correctanswer = correctanswer , verifyanswer = bool((correctanswer == form.answer.data)), regulation = user_experiments[n_reg-1], balance_sheet = user_experiments[n_reg-1], user_id = current_user.id)
        spenttime = ((datetime.utcnow() - session['start_time']))

        headers = ['Index','Regulation','balance_sheet','answer','true','correctanswer','user_id','Student ID','Username', 'Time Elapsed','Submission Time','Score']
        
        if (n_reg == 1):
            if (bool(correctanswer == form.answer.data)):
                Score = 1
            else:
                Score = 0
        else:
            if (bool(correctanswer == form.answer.data)):
                df = pd.read_csv("./app/static/submissions.csv", names=headers)
                Score = df['Score'].iloc[-1]
                Score = int(Score) + 1   
            else:
                df = pd.read_csv("./app/static/submissions.csv", names=headers)
                Score = df['Score'].iloc[-1]
                Score = int(Score)
                
        row = [n_reg, user_experiments[n_reg-1], user_experiments[n_reg-1], submission.answer, submission.verifyanswer, submission.correctanswer, current_user.id, current_user.student_id, current_user.username, str(spenttime), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), datetime.utcnow().strftime("%Y-%m-%d"), Score ]
        with open('./app/static/submissions.csv', "a") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        f.close()

        if n_reg<=9:
            return redirect(url_for("experiment", n_reg=n_reg+1)) #+1))
        else: 
            return redirect(url_for("endpage"))

    session['start_time'] = datetime.utcnow()
    
    return render_template('experiment.html', form = form, user_experiment_id = user_experiments[n_reg-1], n_reg = n_reg, table = table)



@app.route('/endpage')
def endpage():

    headers = ['Index','Regulation','balance_sheet','answer','true','Correct Answer','User ID','Student ID', 'Username', 'Time Elapsed','Submission Full Time', 'Submission Date', 'Score']
    df = pd.read_csv("./app/static/submissions.csv", usecols=[0,3,5,6], names=headers)

    top = df.head(0)
    bottom = df.tail(10)
    concatenated = pd.concat([top,bottom])
    concatenated.reset_index(inplace=True, drop=True)

    concatenated.loc[concatenated['User ID'] == current_user.id].to_html("./app/static/useranswers.htm", index=None)
    table = concatenated.to_html()

    return render_template('endpage.html', table=table)


@app.route('/leaderboard')
def leaderboard():

    headers = ['Index','Regulation','balance_sheet','answer','true','Correct Answer','user_id','Student ID', 'Username', 'Time Elapsed','Submission Full Time', 'Submission Date', 'Score']
    df = pd.read_csv("./app/static/submissions.csv", parse_dates=[9], names = headers)
    table = df.loc[df['Index'] == 10].sort_values(by='Score', ascending=False).to_html("./app/static/leaderboard.htm", index=None)

    return render_template('leaderboard.html', table=table)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
