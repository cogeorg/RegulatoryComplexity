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
def do_run(identifier, input_file_name1, input_file_name2):
    print("<<<<<< WORKING ON: " + input_file_name1 + " " + input_file_name2)

    out_text = ""
    original = []
    updates = []

    input_file1 = open(input_file_name1, 'r')
    input_file2 = open(input_file_name2, 'r')

    for line in input_file1.readlines():
        out_text += line.strip() + "\n"
        original.append(sanitize(line.strip()))
    input_file1.close()

    for line in input_file2.readlines():
        tokens = sanitize(line.strip()).split(";")
        updates.append(tokens)
    input_file2.close()

    to_add = []
    to_delete = []

    for tokens in updates:
        # check that all entries with tokens[3] == identifier are in the file
        if identifier == tokens[2]:
            to_add.append(tokens[1])

        # make sure that no entry with tokens[3] != identifier is in the file
        if identifier == tokens[0] and tokens[0] != tokens[2]:  # update entry
            to_delete.append(tokens[1])
    if True:
        print("  <<< TO_ADD: " + str(len(to_add)))
        print("  <<< TO_DELETE: " + str(len(to_delete)))
        print("")

    # now loop over all additions and add them
    for entry in to_add:
        if entry not in original:
            out_text += entry + "\n"

    out_file = open(input_file_name1, "w")
    out_file.write(out_text)
    out_file.close()

    # now loop over out_text and check for removals
    out_text = ""
    count = 0
    in_file = open(input_file_name1, "r")
    for line in in_file.readlines():
        if sanitize(line.strip()) in to_delete:
            count += 1 # how many lines we drop
        else:
            out_text += line.strip() + "\n"

    print("  <<< # ITEMS DROPPED:" + str(count))
    out_file = open(input_file_name1, "w")
    out_file.write(out_text)
    out_file.close()

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
    identifier = args[1]
    input_file_name1 = args[2]
    input_file_name2 = args[3]

#
# CODE
#
    do_run(identifier, input_file_name1, input_file_name2)
