#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020-07-26

@author: cogeorg@protonmail.com
"""
import sys
import os
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parse_line(line):
    output_text = ""

    if ("(" in line and ")" in line) or "All other assets:" in line:  # asset type, including exception at the end
        line = re.sub('\(\d\) ', '', line.rstrip("\\"))
        line = re.sub(':', '', line)
        output_text += line

    if "Risk weight" in line and "=" in line:  # risk weight
        output_text += line.rstrip("\\").split(" = ")[1].rstrip("\%") + "%"

    return output_text

# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == "__main__":
    input_directory_name = sys.argv[1]
    output_directory_name = sys.argv[2]
    output_text_header = "<html><head></head><body><p style = 'margin-left :1em'>"
    output_text_footer = "</p></body></html>"

    #
    # LOOP
    #
    counter = 0
    for filename in os.listdir(input_directory_name):
        if filename.endswith(".tex"):
            output_text = output_text_header
            input_file_name = os.path.join(input_directory_name, filename)
            output_file_name = os.path.join(output_directory_name, "regulation_" + str(counter) + ".html")

            if False:
                print(bcolors.OKGREEN + "<<< WORKING ON: " + input_file_name + bcolors.ENDC + " --> " + str(counter))
            if True:
                # tokens = input_file_name.split("-")
                print(filename.rstrip(".tex") + ";" + str(counter))

            input_file = open(input_file_name, "r")

            _out_text = ""  # temporary variable to construct compound statements

            for line in input_file.readlines():
                if "Risk weight " in line:
                    output_text += "<br>The weight for <i>" + _out_text + "</i> is: " + parse_line(line.strip())
                    _out_text = ""   # reset temporary out_text
                else:  # forgot this else initially. it matters.
                    _out_text += parse_line(line.strip())


            output_text += output_text_footer  # add footer

            # print(bcolors.OKGREEN + "<<< WRITING TO: " + output_file_name + bcolors.ENDC)
            output_file = open(output_file_name, "w")
            output_file.write(output_text+"\n")
            output_file.close()
            counter += 1
