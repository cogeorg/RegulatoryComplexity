#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from matplotlib import pyplot as plt
import numpy as np
import re

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_file_name, output_file_name):
    arr = []
    out_text = "frequency;num_words;rel_num_words"

    input_file = open(input_file_name, "r")
    for line in input_file.readlines():
        tokens = line.strip().split(";")
        arr.append(int(tokens[2]))

    # loop over the array and count how often 1,2,...max appears
    l = list(arr)
    sum = 0
    for i in range(1,max(arr)):  # sum needs to be computed over all entries
        sum += l.count(i)

    for i in range(1,50):  # we cut off at 50
        _count = l.count(i)
        out_text += str(i) + ";" + str(_count) + ";" + str(float(_count)/float(sum)) + "\n"

    output_file = open(output_file_name, "w")
    output_file.write(out_text)
    output_file.close()


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
    output_dir = "./histograms/" # TODO: this is a hack
    identifier = output_file_name.replace("./histograms/", "").replace(".csv", "")

#
# CODE
#
    count = do_run(input_file_name, output_file_name)

    # Creating histogram

    # fig, ax = plt.subplots(figsize =(10, 7))
    # ax.hist(arr2, bins=20)
    # plt.xlabel("Frequency")
    # plt.ylabel("Number of Operators/Operands")
    # plt.title(identifier)
    # plt.savefig(output_dir + identifier + ".png")
    print(" <<< FINISHED: " + input_file_name + ">>>")
