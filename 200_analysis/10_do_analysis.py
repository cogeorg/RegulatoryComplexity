#!/usr/bin/env python
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
    out_text = "file_name;Attributes;EconomicOperands;GrammaticalOperators;LegalOperators;LegalReferences;LogicalOperators;Other;RegulationOperators"

    count = {}
    count['GrammaticalOperators'] = 0
    count['RegulationOperators'] = 0
    count['Attributes'] = 0
    count['LegalOperators'] = 0
    count['LogicalOperators'] = 0
    count['EconomicOperands'] = 0
    count['LegalReferences'] = 0
    count['Other'] = 0

    for input_file_name in os.listdir(input_dir):
        input_file = open(input_dir + "/" + input_file_name, 'r')

        # reset counter
        for count_key in sorted(count.keys()):
            count[count_key] = 0

        # read html file
        for line in input_file.readlines():
            for count_key in count.keys():
                count[count_key] += line.count(count_key) # for each line, add the total number of occurences
        
        # add output
        out_text += input_file_name
        for count_key in sorted(count.keys()):
            out_text += ";" + str(count[count_key]) 
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