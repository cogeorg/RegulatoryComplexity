from flask import render_template
from flask import request, jsonify
from helper_functions import *
from app import app
import json
import csv
import pandas


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/_array2python')
def array2python():
    wordlist = json.loads(request.args.get('wordlist'))
    time_list, color_list, word_list, place_list = format_list(str(wordlist))
    data = pandas.read_csv('app/output/output.csv', names=['word', 'color'])
    classified_words = data.word.tolist()
    colors_words =data.color.tolist()
    dict_words = dict(zip(classified_words, colors_words))
    for element in time_list:
        index = time_list.index(element)
        word = check_proper_string(word_list[index], place_list[index])
        dict_words[word] = color_list[index][18:]
    classified_words = dict_words.keys()
    colors_words = dict_words.values()

    with open("app/output/output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zip(classified_words, colors_words))

    return jsonify(words = classified_words, colors = colors_words)