#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################
def prepare_line(line):
    line = line.strip()
    line = line.replace("<!DOCTYPE html><html><head></head><body>", "")
    line = line.replace("</body></html>", "")

    line = line.replace('<div class = "', '')
    line = line.replace('<div ', '')
    line = line.replace("</div>", "")

    # pattern = '<span class="EconomicOperands"> class </span> = "ex[0-10]">'
    # line = re.sub(pattern, "", line)
    # OK, I give up. The below works properly
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex0">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex1">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex2">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex3">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex4">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex5">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex6">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex7">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex8">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex9">','')
    line = line.replace('<span class="EconomicOperands"> class </span> = "ex10">','')

    line = line.replace('ex1">', '') # needs to come after the block above
    line = line.replace('ex2">', '')
    line = line.replace('ex3">', '')
    line = line.replace('ex4">', '')
    line = line.replace('ex5">', '')
    line = line.replace('ex6">', '')
    line = line.replace('ex7">', '')
    line = line.replace('ex8">', '')
    line = line.replace('ex9">', '')
    line = line.replace('ex10">', '')

    line = re.sub('^\.', "", line)

    return line


# ENSURE THAT THIS METHOD IS THE SAME AS IN 13_STANDARDIZE_MASTER.PY
def clean(value):
    value = value.replace("\n", "")

    value = value.replace("'", "")
    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.replace(";", "")
    value = value.replace(":", "")
    value = value.replace('"', '')
    value = value.replace("`", "")
    value = value.replace("$", "")

    value = value.replace("(", "")
    value = value.replace(")", "")

    value = value.replace("``", "")
    value = value.replace("--", "")

    value = value.upper()

    return value


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, dict_file_name, output_dir):
    dict = {}

    print("<<< 14_COUNT_HTML_NOCLASS.PY")

    #
    # LOAD CONSOLIDATED DICTIONARY
    #
    dict_file = open(dict_file_name, "r")
    dict_file.readline()  # ignore header
    for line in dict_file.readlines():
        tokens = line.strip().split(";")
        dict[tokens[0].strip('"')] = tokens[1].strip('"').strip()
    print("  <<< READ DICTIONARY: " + dict_file_name + " WITH " + str(len(dict)) + " ENTRIES")

    # dict.sort(key=len, reverse=True)

    if False:
        for key in sorted(dict, key=len, reverse=True):
            print(key, "-->", dict[key])

    #
    # LOOP OVER ALL FILES IN DIRECTORY AND FIND OCCURRENCE OF EACH DICT ENTRY
    #
    for input_file_name in os.listdir(input_dir):
        in_text = ""
        out_text = ""

        input_file = open(input_dir + "/" + input_file_name, 'r')
        out_file = open(output_dir + "/" + "cons-count_" + input_file_name.rstrip(".html") + ".csv", 'w')
        residual_file = open(output_dir + "/" + "residual_cons-count_" + input_file_name.rstrip(".html") + ".csv", 'w')

        print("  <<< NOW WORKING ON: " + input_dir + input_file_name)

        for line in input_file.readlines():
            in_text += clean(prepare_line(line.strip()))

        for key in sorted(dict, key=len, reverse=True):
            _count = in_text.count(key)
            if _count > 0:
                out_text += key + ";" + dict[key] + ";" + str(_count) + "\n"
                in_text = in_text.replace(key, "")

        if False:
            print(in_text)

        out_file.write(out_text)
        out_file.close()
        residual_file.write(in_text)
        residual_file.close()

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
