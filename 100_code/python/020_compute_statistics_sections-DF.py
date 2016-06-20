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
    line = re.sub("\n", "", line)  # remove newlines
    line = re.sub(r"  *", " ", line)  # remove repeated whitespaces
    line = re.sub(r"--", "", line)  # remove double dashes
    #line = re.sub(r"&lt;&lt;(NOTE:.*)&gt;&gt;\s*" , "", line)  # remove all document notes
    return line


# -------------------------------------------------------------------------
def do_analysis(lines, matches, out_directory):
    results = {}

    # clean lines first
    line = clean_line(lines)

    print "LENGTH BEFORE: " + str(len(line))

    tmp_array = matches.keys()
    tmp_array.sort(key = lambda s: -len(s))

    for entry in tmp_array:
        [line, num_replacements] = re.subn(" " + entry, "", line)

        try:
            results[matches[entry]] += int(num_replacements)
        except:
            results[matches[entry]] = int(num_replacements)

        out_file_name = out_directory + str(matches[entry]) + ".csv"
        out_file = open(out_file_name, "a")
        out_file.write(entry + ";" + str(num_replacements) + "\n")
        out_file.close()
        

    results_file_name = out_directory + "results.csv"
    results_file = open(results_file_name, 'w')
    for key in results.keys():
        results_file.write(key + ";" + str(results[key]) + "\n")
    results_file.close()

    print "LENGTH AFTER: " + str(len(line))
    out_file_name = out_directory + "remaining_text.txt"
    out_file = open(out_file_name, 'w')
    out_file.write(line)
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
    out_directory = sys.argv[3]  # statistics are written to the out directory but have the same name as the in file

    # now do the actual analysis of the string containing all the lines of the input file
    do_analysis(lines, matches, out_directory)
