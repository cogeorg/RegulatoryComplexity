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

    total_words = 0
    total_classified = 0

    Attributes = []
    input_file = open("../020_word_lists/Attributes.txt")
    for line in input_file.readlines():
        Attributes.append(line.strip())

    EconomicOperands = []
    input_file = open("../020_word_lists/EconomicOperands.txt")
    for line in input_file.readlines():
        EconomicOperands.append(line.strip())

    FunctionWords = []
    input_file = open("../020_word_lists/FunctionWords.txt")
    for line in input_file.readlines():
        FunctionWords.append(line.strip())

    LegalReferences = []
    input_file = open("../020_word_lists/LegalReferences.txt")
    for line in input_file.readlines():
        LegalReferences.append(line.strip())

    LogicalConnectors = []
    input_file = open("../020_word_lists/LogicalConnectors.txt")
    for line in input_file.readlines():
        LogicalConnectors.append(line.strip())

    Other = []
    input_file = open("../020_word_lists/Other.txt")
    for line in input_file.readlines():
        Other.append(line.strip())

    RegulatoryOperators = []
    input_file = open("../020_word_lists/RegulatoryOperators.txt")
    for line in input_file.readlines():
        RegulatoryOperators.append(line.strip())

    if False:
        print(Attributes)
        print(EconomicOperands)
        print(FunctionWords)
        print(LegalReferences)
        print(LogicalConnectors)
        print(Other)
        print(RegulatoryOperators)

    print("<<<<<< WORKING ON: " + input_file_name)

    if True:
        print("  READING WORDS")
        print("    # Attributes: " + str(len(Attributes)))
        print("    # EconomicOperands: " + str(len(EconomicOperands)))
        print("    # FunctionWords: " + str(len(FunctionWords)))
        print("    # LegalReferences: " + str(len(LegalReferences)))
        print("    # LogicalConnectors: " + str(len(LogicalConnectors)))
        print("    # Other: " + str(len(Other)))
        print("    # RegulatoryOperators: " + str(len(RegulatoryOperators)))

    input_file = open(input_file_name, 'r')

    # read .txt file
    for line in input_file.readlines():
        tokens = line.strip().split(" ")
        for token in tokens:
            is_classified = False
            if token in Attributes:
                is_classified = True
                count['Attributes'] += 1
            if token in EconomicOperands:
                is_classified = True
                count['EconomicOperands'] += 1
            if token in FunctionWords:
                is_classified = True
                count['FunctionWords'] += 1
            if token in LegalReferences:
                is_classified = True
                count['LegalReferences'] += 1
            if token in LogicalConnectors:
                is_classified = True
                count['LogicalConnectors'] += 1
            if token in Other:
                is_classified = True
                count['Other'] += 1
            if token in RegulatoryOperators:
                is_classified = True
                count['RegulatoryOperators'] += 1

            total_words += 1
            if is_classified:
                total_classified += 1
    print("  TOTAL WORDS: " + str(total_words))
    print("  TOTAL CLASSIFIED: " + str(total_classified))
    frac = float(total_classified)/float(total_words)
    print("  FRACTION CLASSIFIED: " + str(round(frac,2)))

    # add output
    out_text += input_file_name
    # for count_key in sorted(count.keys()):
    #     out_text += ";" + str(count[count_key]) + ";" + str(len(set(unique[count_key]))) # TODO: doesn't work yet.
    out_text += "\n"


    out_file = open(output_file_name, 'w')
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
    input_file_name = args[1]
    output_file_name = args[2]

#
# CODE
#
    do_run(input_file_name, output_file_name)
