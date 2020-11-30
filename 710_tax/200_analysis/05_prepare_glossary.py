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
    out_text = ""

    print("<<<<<< WORKING ON: " + input_file_name)

    input_file = open(input_file_name, 'r')

    # read .txt file
    for line in input_file.readlines():
        tokens = line.strip().split("--")
        out_text += tokens[0].strip() + "\n"

    # add output
    out_text += "\n"

    out_file = open(output_file_name, 'w')
    out_file.write(out_text)
    out_file.close()
    print("    >>> FILE WRITTEN TO:" + output_file_name)
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
    input_file_name = args[1]
    output_file_name = args[2]

#
# CODE
#
    do_run(input_file_name, output_file_name)
