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


def clean(value):
    value = value.replace("'", "")
    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.replace(";", "")
    value = value.replace(":", "")
    value = value.replace('"', '')
    value = value.replace("`", "")

    # value = value.replace("(", "")
    # value = value.replace(")", "")

    value = value.replace("``", "")
    value = value.replace("--", "")

    return value


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, output_dir):
    print("<<< 12_COUNT_HTML.PY")

    #
    # LOOP OVER ALL FILES IN DIRECTORY AND FIND OCCURRENCE OF EACH DICT ENTRY
    #
    for input_file_name in os.listdir(input_dir):
        unique = {}
        count = {}

        in_text = ""
        out_text = ""

        residual_tokens = []
        residual_text = ""

        input_file = open(input_dir + "/" + input_file_name, 'r')
        out_file = open(output_dir + "/results_" + input_file_name.rstrip(".html") + ".csv", 'w')
        res_file = open(output_dir + "/residual_" + input_file_name.rstrip(".html") + ".txt", 'w')

        for line in input_file.readlines():
            in_text += line.strip()
            line = prepare_line(line)

            tokens = line.split(" ")  # split the line along spans, losing the <span class= itself

            # iterate over this array of tokens
            _start = False
            _end = False
            for token in tokens:
                if token == "<span":
                    _start = True
                if token == "</span>":
                    _end = True
                if _start:
                    if "class=" in token:
                        value = token.lstrip('class="').rstrip('">')
                    else:
                        if not _end:
                            key = clean(token.strip())

                if not _start:
                    residual_tokens.append(token.strip())

                if _end:  # closed an entry, add to dicts
                    if key != "":
                        unique[key] = value
                        try: # see if we can update the count
                            count[key] += 1
                        except KeyError:
                            count[key] = 1

                    _start = False
                    _end = False

        input_file.close()

        if False:
            for key in count.keys():
                print(key, count[key], unique[key])

        print("  <<< WORKED ON: " + input_dir + input_file_name + " WITH " + str(len(unique.keys())) + " UNIQUE KEYS FOUND AND " + str(len(residual_tokens)) + " KEYS NOT FOUND")

        for key in unique.keys():
            out_text += key + ";" + unique[key] + ";" + str(count[key]) + "\n"

        out_file.write(out_text)
        out_file.close()

        for token in residual_tokens:
            residual_text += clean(token) + "\n"
        res_file.write(residual_text)
        res_file.close()


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
    output_file_name = args[2]

#
# CODE
#
    do_run(input_dir, output_file_name)
