from flask import render_template
from flask import request, jsonify
from helper_functions import *
from app import app
import json
import csv
import pandas
import glob
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/title_1')
def title_1():
    return render_template('title_1.html')


@app.route('/title_2')
def title_2():
    return render_template('TITLE II--ORDERLY LIQUIDATION AUTHORITY.html')


@app.route('/title_3')
def title_3():
    return render_template('TITLE III--TRANSFER OF POWERS TO THE COMPTROLLER OF THE CURRENCY, THE CORPORATION, AND THE BOARD OF GOVERNORS.html')


@app.route('/title_4')
def title_4():
    return render_template('TITLE IV--REGULATION OF ADVISERS TO HEDGE FUNDS AND OTHERS.html')


@app.route('/title_5')
def title_5():
    return render_template('TITLE V--INSURANCE.html')



@app.route('/title_6')
def title_6():
    return render_template('TITLE VI--IMPROVEMENTS TO REGULATION OF BANK AND SAVINGS ASSOCIATION HOLDING COMPANIES AND DEPOSITORY INSTITUTIONS.html')


@app.route('/title_7')
def title_7():
    return render_template('TITLE VII--WALL STREET TRANSPARENCY AND ACCOUNTABILITY.html')



@app.route('/title_8')
def title_8():
    return render_template('TITLE VIII--PAYMENT, CLEARING, AND SETTLEMENT SUPERVISION.html')



@app.route('/title_9')
def title_9():
    return render_template('TITLE IX--INVESTOR PROTECTIONS AND IMPROVEMENTS TO THE REGULATION OF SECURITIES.html')



@app.route('/title_10')
def title_10():
    return render_template('TITLE X-- BUREAU OF CONSUMER FINANCIAL PROTECTION.html')



@app.route('/title_11')
def title_11():
    return render_template('TITLE XI--FEDERAL RESERVE SYSTEM PROVISIONS.html')



@app.route('/title_12')
def title_12():
    return render_template('TITLE XII--IMPROVING ACCESS TO MAINSTREAM FINANCIAL INSTITUTIONS.html')



@app.route('/title_13')
def title_13():
    return render_template('TITLE XIII--PAY IT BACK ACT.html')




@app.route('/title_14')
def title_14():
    return render_template('TITLE XIV-- MORTGAGE REFORM AND ANTI-PREDATORY LENDING ACT.html')



@app.route('/title_15')
def title_15():
    return render_template('TITLE XV--MISCELLANEOUS PROVISIONS.html')








@app.route('/_array2python')
def array2python():
    params = json.loads(request.args.get('params'))
    user_name = params['user_name']
    wordlist = params['wordList']

    actual_file= glob.glob("app/output/*.csv")
    data = pandas.read_csv(actual_file[0], names=['word', 'color'])
    classified_words = data.word.tolist()
    colors_words =data.color.tolist()
    dict_words = dict(zip(classified_words, colors_words))
    for element in wordlist:
            word = element.split("_")[0]
            word = word.strip()
            word = word.lower()
            dict_words[word] = element.split("_")[1]
    classified_words = dict_words.keys()
    colors_words = dict_words.values()
    file = "app/output/" + user_name + ".csv"
    print file

    with open(file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zip(classified_words, colors_words))

    if actual_file[0] != file:
        os.remove(actual_file[0])
    return jsonify(words = classified_words, colors = colors_words)