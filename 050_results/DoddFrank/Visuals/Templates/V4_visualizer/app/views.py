from flask import render_template
from flask import request, jsonify
from app import app
import json
import csv
import pandas
from math import isnan


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/_array2python')
def array2python():
    wordlist = json.loads(request.args.get('wordlist'))
    if wordlist == []:
        wordlist = ["dummyvariable_green"]
    data = pandas.read_csv('app/output/output.csv', names=['word', 'color'])
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



    with open("app/output/output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zip(classified_words, colors_words))
    return jsonify(words = classified_words, colors = colors_words)
