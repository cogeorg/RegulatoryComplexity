#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:10:43 2019

@author: jane
"""
from flask import render_template, flash, redirect, request, url_for, send_file, session
from flask_login import current_user, login_user
from app.models import User, Submission
from app import app, db
from app.forms import LoginForm, RegistrationForm, RulesForm, SubmissionForm
from flask_login import login_required, logout_user
from werkzeug.urls import url_parse
import csv
from datetime import datetime


@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html')

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
        flash('You are now a registered user!')
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
def experiment(n_reg=1):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user_id = current_user.id
    user_experiments = []
    for line in open("./app/static/users/user_" + str(user_id) + "_experiments.csv"):
        user_experiments.append(line.strip("\n"))

    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(answer = form.answer.data, regulation = user_experiments[n_reg-1], balance_sheet= user_experiments[n_reg-1], user_id = current_user.id)
        spenttime = datetime.utcnow() - session['start_time']
        row = [user_experiments[n_reg-1], user_experiments[n_reg-1], submission.answer, current_user.id, current_user.student_id, str(spenttime), str(datetime.utcnow()) ]
        with open('./app/static/submissions.csv', "a") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        f.close()

        if n_reg<=9:
            return redirect(url_for("experiment", n_reg=n_reg+1)) #+1))
        else:
            return redirect(url_for("endpage"))

    session['start_time'] = datetime.utcnow()
    return render_template('experiment.html', form = form, user_experiment_id = user_experiments[n_reg-1], n_reg = n_reg)


@app.route("/endpage")
def endpage():
    return render_template("endpage.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
