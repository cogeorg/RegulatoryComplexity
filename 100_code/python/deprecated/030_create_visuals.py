#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import re
import sys
import os


# ------------------------------------------------------------------------- 
def write_text_to_file(out_text, out_directory, line):
    # first, get the out_file_name
    identifier = line.lstrip('SEC. ').split(' ')[0].rstrip('.')
    out_file_name = out_directory + identifier + ".txt"

    out_file = open(out_file_name, 'w')
    out_file.write(out_text)
    out_file.close()



# -------------------------------------------------------------------------
def clean_line(line):
    line = re.sub(r"\n", "", line)  # remove newlines
    line = re.sub(r"  *", " ", line)  # remove repeated whitespaces
    line = re.sub(r"--", "", line)  # remove double dashes
    
    #line = re.sub("[^A-Za-z0-9 ]", "", line)
    #line = re.sub(r"&lt;&lt;(NOTE:.*)&gt;&gt;\s*" , "", line)  # remove all document notes
    return line.lower()


# -------------------------------------------------------------------------
def get_header(in_file_name):
    text = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>"""
    text += in_file_name
    text += """</title>
    </head>
    <body>
    """
    text += "<h1>" + in_file_name + "</h1>\n"
    return text


# -------------------------------------------------------------------------
def get_footer():
    text = """
    </body>
    </html>
    """
    return text


# -------------------------------------------------------------------------
def do_analysis(in_file_name, match_directory, lines, matches, out_file_name):
    results = {}
    styles = {
        "GrammaticalOperators"  : 'background-color: #554600;',
        "LegalOperators"        : 'background-color: #806D15;',
        "LegalReferences"       : 'background-color: #D4C26A;',
        "LogicalOperators"      : 'background-color: #FFF0AA;',
        "RegulationOperators"   : 'background-color: #AA0739;',
        "Attributes"            : 'background-color: green;',
        "EconomicOperands"      : 'background-color: yellow;',
        "Other"                 : 'background-color: red;'
    }

    # start creating the website output
    out_text = get_header(in_file_name)

    # clean lines first
    line = clean_line(lines)
    
    tmp_array = matches.keys()
    tmp_array.sort(key = lambda s: -len(s))

    for entry in tmp_array:
        to_replace = clean_line(" " + entry)
        replacement = " <text style='" + styles[matches[entry]] + "'>" + entry + "</text>"
        line = re.sub(to_replace, replacement, line.lower())

    out_text += line

    out_text += get_footer()

    out_file = open(out_file_name, 'w')
    out_file.write(out_text)
    out_file.close()
    #print line


# -------------------------------------------------------------------------
def construct_matches(match_directory):
    matches = {}  # matches = {identifier: [list of words]}
    match_listing = os.listdir(match_directory)

    for match_file_name in match_listing:
        match_file = open(match_directory + match_file_name)
        for line in match_file.readlines():
            matches[line.strip()] = match_file_name.split(".")[0]

    return matches


# -------------------------------------------------------------------------
#
#  
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
    in_file_name = sys.argv[1]
    f = open(in_file_name)
    lines = f.read()
    line_array = lines.split('\n')
    
    match_directory = sys.argv[2]  # the directory where the files are that contain the words we are looking for
    matches = construct_matches(match_directory)

    # results will be stored in out_directory    
    out_file_name = sys.argv[3]  # statistics are written to the out directory but have the same name as the in file

    # now do the actual analysis of the string containing all the lines of the input file
    do_analysis(in_file_name, match_directory, lines, matches, out_file_name)
