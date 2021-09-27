#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os


# ###########################################################################
# METHODS
# ###########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, output_file_name):
    out_text = "file_name;Attributes;UniqueAttributes;EconomicOperands;UniqueEconomicOperands;FunctionWords;UniqueFunctionWorsd;LegalReferences;UniqueLegalReferences;LogicalConnectors;UniqueLogicalConnectors;Other;UniqueOther;RegulatoryOperators;UniqueRegulatoryOperators\n"

    count = {}
    count['Attributes'] = 0
    count['EconomicOperands'] = 0
    count['FunctionWords'] = 0
    count['LegalReferences'] = 0
    count['LogicalConnectors'] = 0
    count['Other'] = 0
    count['RegulatoryOperators'] = 0

    unique = {}
    unique['Attributes'] = []
    unique['EconomicOperands'] = []
    unique['FunctionWords'] = []
    unique['LegalReferences'] = []
    unique['LogicalConnectors'] = []
    unique['Other'] = []
    unique['RegulatoryOperators'] = []

    print("<<< STARTING 10_DO_ANALYSIS.PY")

    for input_file_name in os.listdir(input_dir):
        input_file = open(input_dir + "/" + input_file_name, 'r')

        # reset counter
        for count_key in sorted(count.keys()):
            count[count_key] = 0
            unique[count_key] = []

        print("  <<< NOW WORKING ON: " + input_dir + input_file_name)
        # read html file
        for line in input_file.readlines():
            for count_key in count.keys():
                count[count_key] += line.count(count_key) # for each line, add the total number of occurences
                tokens = line.split("<span class=")  # split the line along spans
                for token in tokens:
                	token2 = token.split("</span>")[0].split('">')  # and split the opening of a span by the closing of a span
                	try:
                		this_key = token2[0].lstrip('"')  # strip off some stuff, we are left with the count_key
                		this_value = token2[1].lstrip().rstrip()  # for each key, we have a value
                		try:
                			unique[this_key].append(this_value)
                		except:
                			pass
                	except IndexError:
                		pass
        # add output
        out_text += input_file_name
        for count_key in sorted(count.keys()):
            out_text += ";" + str(count[count_key]) + ";" + str(len(set(unique[count_key]))) # TODO: doesn't work yet.
        out_text += "\n"


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
    output_file_name = args[2]

#
# CODE
#
    do_run(input_dir, output_file_name)
