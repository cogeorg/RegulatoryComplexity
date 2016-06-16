#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import re
import sys

# ------------------------------------------------------------------------- 
def replace_indents(text):
    # replace indentations for some sections
    regexp =  r"&lt;&lt;(.*)&gt;&gt;\s*" 
    text  = re.sub(regexp,'', text)
    return text

# ------------------------------------------------------------------------- 
def write_text_to_file(out_text, out_directory, line):
    # first, get the out_file_name
    identifier = line.lstrip('SEC. ').split(' ')[0].rstrip('.')
    out_file_name = out_directory + identifier + ".txt"
    
    out_file = open(out_file_name, 'w')
    out_file.write(out_text)
    out_file.close()


# -------------------------------------------------------------------------
#
#  
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
    in_file_name = sys.argv[1]
    f = open(in_file_name)
    lines = f.read()
    print lines
    line_array = lines.split('\n')
    
    print len(line_array)