#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re
import fnmatch

# ###########################################################################
# METHODS
# ###########################################################################

def clean(value):
    value = value.replace("``", "")
    value = value.replace("--", "")
    value = value.replace("&lt;", "<")
    value = value.replace("&gt;", ">")

    tokens = value.split("[[Page")
    if len(tokens) > 1:
        value = ""

    return value


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, dict_file_name, output_dir):
    out_text = ""

    dict = []

    print("<<< 12_COUNT_TXT.PY")

    #
    # LOAD DICTIONARY
    #
    dict_file = open(dict_file_name, "r")
    for line in dict_file.readlines():
        tokens = line.strip().split(";")
        dict.append(tokens[0].strip())
    print("  <<< READ DICTIONARY: " + dict_file_name + " WITH " + str(len(dict)) + " ENTRIES")

    dict.sort(key=len, reverse=True)

    #
    # LOOP OVER ALL FILES IN DIRECTORY AND FIND OCCURRENCE OF EACH DICT ENTRY
    #
    for input_file_name in os.listdir(input_dir):
        input_file = open(input_dir + "/" + input_file_name, 'r')
        out_file = open(output_dir + "/" + input_file_name, 'w')

        print("  <<< NOW WORKING ON: " + input_dir + input_file_name)
        in_text = ""
        for line in input_file.readlines():
            in_text += clean(line.strip()) + " " # instead of newlines, add a whitespace
        in_text = re.sub("\s+", " ", in_text)  # replace all duplicate whitespaces that come from newlines

        for token in dict:
            # find all occurences of the token in the text
            if False:
                print(token, in_text.count(token))
            out_text += token + ";" + str(in_text.count(token)) + "\n"
            # then remove the occurrences from the text
            in_text = in_text.replace(token, "")

        out_file.write(out_text)
        out_file.close()


# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#
#  MAIN
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    input_dir = args[1]
    dict_file_name = args[2]
    output_file_name = args[3]

#
# CODE
#
    do_run(input_dir, dict_file_name, output_file_name)
