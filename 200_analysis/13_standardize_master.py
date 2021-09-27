#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################

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
def do_run(input_file_name, output_file_name):
    out_text = ""
    dict_in = {}
    dict_cons = {}

    print("<<< 13_STANDARDIZE_MASTER.PY")

    #
    # LOAD DICTIONARY
    #
    dict_file = open(input_file_name, "r")
    for line in dict_file.readlines():
        tokens = line.strip().split(";")
        try:
            dict_in[tokens[0].strip('"')] = tokens[1].strip('"')
        except:
            pass
    print("  <<< READ DICTIONARY: " + input_file_name + " WITH " + str(len(dict_in)) + " ENTRIES")

    for key in dict_in.keys():
        dict_cons[key] = clean(key)

    for key in dict_cons.keys():
        out_text += key + ";" + dict_cons[key] + ";" + dict_in[key] + "\n"

    out_file = open(output_file_name, "w")
    out_file.write(out_text)
    out_file.close()

    print("  <<< WRITTEN DICTIONARY TO: " + output_file_name)

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
    input_file_name = args[1]
    output_file_name = args[2]

#
# CODE
#
    do_run(input_file_name, output_file_name)
