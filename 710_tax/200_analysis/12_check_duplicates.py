#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re

# ###########################################################################
# METHODS
# ###########################################################################
def sanitize(entry):
    entry = entry.upper()
    #
    # # remove all links to other sections
    # numbers = re.findall(r'([0-9]+)\.', entry)  # needs to be done before replacing "."
    # for number in numbers:
    #     entry = entry.replace(number, "")
    #
    # entry = entry.replace("'", "")
    # entry = entry.replace('"', '')
    # entry = entry.replace('`', '')
    # entry = entry.replace(",", "")
    # entry = entry.replace(".", "")
    # entry = entry.replace(":", "")
    # entry = entry.replace(";", "")
    # entry = entry.replace("(", "")
    # entry = entry.replace(")", "")
    # entry = entry.replace("[", "")
    # entry = entry.replace("]", "")
    # entry = entry.replace("%", "")
    # entry = entry.replace("-", "")
    # entry = entry.replace("$", "")
    #
    # numbers = re.findall(r'([0-9]+)', entry)  # needs to be done before replacing "."
    # for number in numbers:
    #     entry = entry.replace(number, "")

    return entry

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_file_name1, input_file_name2):
    print("<<<<<< WORKING ON: " + input_file_name1 + " " + input_file_name2)

    original = []
    compare = []

    input_file1 = open(input_file_name1, 'r')
    input_file2 = open(input_file_name2, 'r')

    for line in input_file1.readlines():
        original.append(sanitize(line.strip()))
    input_file1.close()

    for line in input_file2.readlines():
        compare.append(sanitize(line.strip()))
    input_file2.close()

    for entry in compare:
        if entry in original:
            print(entry)
    print(">>>>>> FINISHED")
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
    input_file_name1 = args[1]
    input_file_name2 = args[2]

#
# CODE
#
    do_run(input_file_name1, input_file_name2)
