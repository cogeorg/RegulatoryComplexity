#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os

# ###########################################################################
# METHODS
# ###########################################################################

def clean(value):
    value = value.replace("'", "")
    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.replace(";", "")
    value = value.replace(":", "")
    value = value.replace('"', '')
    value = value.replace("`", "")

    value = value.replace("(", "")
    value = value.replace(")", "")

    value = value.replace("``", "")
    value = value.replace("--", "")

    return value


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, dict_file_name, output_file_name):
    out_text = ""

    unique = {}

    #
    # LOOP OVER ALL FILES TWICE, FIRST TO READ ALL WORDS, THEN TO COUNT THEM
    #
    for input_file_name in os.listdir(input_dir):
        input_file = open(input_dir + "/" + input_file_name, 'r')

        print("  <<< NOW WORKING ON: " + input_dir + input_file_name)

        # read html file
        for line in input_file.readlines():
            tokens = line.split("<span class=")  # split the line along spans
            for token in tokens:
                token2 = token.split("</span>")[0].split('">')  # and split the opening of a span by the closing of a span
                try:
                    this_key = clean(token2[1].lstrip().rstrip())  # for each key, we have a value
                    this_value = token2[0].lstrip('"')  # strip off some stuff, we are left with the count_key
                    unique[this_key] = this_value
                except:
                    pass

    #
    # WRITE DICTIONARY
    #
    for key in unique.keys():
        print(key + ";" + unique[key])
        out_text += key + ";" + unique[key] + "\n"

    out_file = open(dict_file_name, 'w')
    out_file.write(out_text)
    out_file.close()

    # for input_file_name in os.listdir(input_dir):
    #     input_file = open(input_dir + "/" + input_file_name, 'r')
    #
    #     print("  <<< NOW WORKING ON: " + input_dir + input_file_name)
    #
    #     # read html file
    #     for line in input_file.readlines():
    #         for count_key in count.keys():
    #             count[count_key] += line.count(count_key) # for each line, add the total number of occurences
    #     # add output
    #     out_text += input_file_name
    #     for count_key in sorted(count.keys()):
    #         out_text += ";" + str(count[count_key]) + ";" + str(len(set(unique[count_key]))) # TODO: doesn't work yet.
    #     out_text += "\n"


    out_file = open(output_file_name, 'w')
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
