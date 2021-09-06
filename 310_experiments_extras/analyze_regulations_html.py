#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020-07-26

@author: cogeorg@protonmail.com
"""
import sys
import os
import re

import numpy as np

from collections import defaultdict

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

multi_tokens = [
    "Capital Instrument",
    "multilateral development bank",
    "public sector",
    "Real Estate",
    "central government",
    "asset maturity",
    "Fixed Asset",
    "national currency",
    "OECD State",
    "central bank",
    "OECD country",
    "public-sector entity",
    "public sector entities"
]

def clean_file(input_file):
    in_text = ""

    for line in input_file.readlines():
        in_text += line.rstrip()  # single line only
    # strip header and footer
    in_text = in_text.replace(header, "")
    in_text = in_text.replace(footer, "")
    in_text = in_text.lstrip("<br>")
    in_text = in_text.replace("<i>", "")
    in_text = in_text.replace("</i>", "")
    in_text = in_text.replace("<br>", " ")
    in_text = in_text.replace("  ", " ")
    in_text = in_text.replace(":", "")

    return in_text

id_file = {}
id_token = {}

# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    input_directory_name = sys.argv[1]
    output_file_name = sys.argv[2]

    header = "<html><head></head><body><p style = 'margin-left :1em'>"
    footer = "</p></body></html>"

    file_counter = 0
    token_counter = 0

    #
    # PREPARE DICTIONARIES
    #
    for filename in os.listdir(input_directory_name):
        if filename.endswith(".html"):
            identifier = filename.rstrip(".html").split("_")[1]
            id_file[identifier] = file_counter
            file_counter += 1

            input_file_name = os.path.join(input_directory_name, filename)
            input_file = open(input_file_name, "r")
            # print("<<< WORKING ON: " + bcolors.OKGREEN + input_file_name + bcolors.ENDC)

            if False:
                print(in_text + "\n")
            in_text = clean_file(input_file)

            # don't delete elements of an array you iterate over
            _tmp_tokens = []
            for _tmp_token in multi_tokens:
                _tmp_tokens.append(_tmp_token)

            for token in _tmp_tokens:
                if token in in_text:
                    id_token[token] = token_counter
                    token_counter += 1
                    multi_tokens.remove(token) # delete token counter from array

            for token in in_text.split(" "):
                if token not in id_token.keys():
                    id_token[token] = token_counter
                    token_counter += 1

    #
    # COMPUTE RESULTS
    #
    if False:  # debugging
        for key in id_file.keys():
            print(key, id_file[key])
        for key in sorted(id_token, key=len, reverse=True):
            print(key, id_token[key])

    _rows = len(id_token.keys())
    _cols = len(id_file.keys())
    results = np.zeros( (_rows,  _cols) )

    file_counter = 0
    token_counter = 0

    for filename in os.listdir(input_directory_name):
        if filename.endswith(".html"):
            identifier = filename.rstrip(".html").split("_")[1]

            input_file_name = os.path.join(input_directory_name, filename)
            input_file = open(input_file_name, "r")
            print("<<< WORKING ON: " + bcolors.OKGREEN + input_file_name + bcolors.ENDC)

            if False:
                print(in_text + "\n")
            in_text = clean_file(input_file)

            for token in sorted(id_token, key=len, reverse=True):
                results[id_token[token]][id_file[identifier]] = in_text.count(token)
                if token in in_text:
                    in_text = in_text.replace(token, "")

    #
    # WRITE TEXT OUT
    #
    out_text = ";"
    for filename in os.listdir(input_directory_name):
        if filename.endswith(".html"):
            identifier = filename.rstrip(".html").split("_")[1]
            out_text += str(identifier) + ";"
    out_text += "\n"

    for token in sorted(id_token, key=len, reverse=True):
        out_text += token + ";"
        for filename in os.listdir(input_directory_name):
            if filename.endswith(".html"):
                identifier = filename.rstrip(".html").split("_")[1]
                out_text += str(results[id_token[token]][id_file[identifier]]) + ";"
        out_text += "\n"

    out_file = open(output_file_name, "w")
    out_file.write(out_text)
    out_file.close()
