#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os


# ###########################################################################
# METHODS
# ###########################################################################
def sanitize(entry):
    entry = entry.upper()
    entry = entry.replace(",", "")
    entry = entry.replace(".", "")
    entry = entry.replace(":", "")
    entry = entry.replace(";", "")
    return entry

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(input_dir, output_file_name):
    out_text = "file_name;Attributes;UniqueAttributes;EconomicOperands;UniqueEconomicOperands;FunctionWords;UniqueFunctionWorsd;LegalReferences;UniqueLegalReferences;LogicalConnectors;UniqueLogicalConnectors;Other;UniqueOther;RegulatoryOperators;UniqueRegulatoryOperators;num_operators;num_operands;num_unique_operators;num_unique_operands;total_volume;potential_volume;level\n"

    count = {}
    count['Attributes'] = 0
    count['EconomicOperands'] = 0
    count['FunctionWords'] = 0
    count['LegalReferences'] = 0
    count['LogicalConnectors'] = 0
    count['Other'] = 0
    count['RegulatoryOperators'] = 0
    count['TaxOperands'] = 0

    unique = {}
    unique['Attributes'] = []
    unique['EconomicOperands'] = []
    unique['FunctionWords'] = []
    unique['LegalReferences'] = []
    unique['LogicalConnectors'] = []
    unique['Other'] = []
    unique['RegulatoryOperators'] = []
    unique['TaxOperands'] = []
    unique['unclassified'] = []

    total_words = 0
    total_classified = 0

    Attributes = []
    input_file = open("../020_word_lists/Attributes.txt")
    for line in input_file.readlines():
        Attributes.append(line.strip().upper())

    EconomicOperands = []
    input_file = open("../020_word_lists/EconomicOperands.txt")
    for line in input_file.readlines():
        EconomicOperands.append(line.strip().upper())

    FunctionWords = []
    input_file = open("../020_word_lists/FunctionWords.txt")
    for line in input_file.readlines():
        FunctionWords.append(line.strip().upper())

    LegalReferences = []
    input_file = open("../020_word_lists/LegalReferences.txt")
    for line in input_file.readlines():
        LegalReferences.append(line.strip().upper())

    LogicalConnectors = []
    input_file = open("../020_word_lists/LogicalConnectors.txt")
    for line in input_file.readlines():
        LogicalConnectors.append(line.strip().upper())

    Other = []
    input_file = open("../020_word_lists/Other.txt")
    for line in input_file.readlines():
        Other.append(line.strip().upper())

    RegulatoryOperators = []
    input_file = open("../020_word_lists/RegulatoryOperators.txt")
    for line in input_file.readlines():
        RegulatoryOperators.append(line.strip().upper())

    TaxOperands = []
    input_file = open("../020_word_lists/TaxOperands.txt")
    for line in input_file.readlines():
        TaxOperands.append(line.strip().upper())

    if False:
        print(Attributes)
        print(EconomicOperands)
        print(FunctionWords)
        print(LegalReferences)
        print(LogicalConnectors)
        print(Other)
        print(RegulatoryOperators)
        print(TaxOperands)

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
        print("    # TaxOperands: " + str(len(TaxOperands)))

    input_file = open(input_file_name, 'r')

    # read .txt file
    for line in input_file.readlines():
        tokens = line.strip().split(" ")
        for entry in tokens:
            token = sanitize(entry)
            is_classified = False

            if token in Attributes:
                is_classified = True
                count['Attributes'] += 1
                try:
                    unique['Attributes'].append(token)
                except:
                    pass

            if token in EconomicOperands:
                is_classified = True
                count['EconomicOperands'] += 1
                try:
                    unique['EconomicOperands'].append(token)
                except:
                    pass

            if token in FunctionWords:
                is_classified = True
                count['FunctionWords'] += 1
                try:
                    unique['FunctionWords'].append(token)
                except:
                    pass

            if token in LegalReferences:
                is_classified = True
                count['LegalReferences'] += 1
                try:
                    unique['LegalReferences'].append(token)
                except:
                    pass

            if token in LogicalConnectors:
                is_classified = True
                count['LogicalConnectors'] += 1
                try:
                    unique['LogicalConnectors'].append(token)
                except:
                    pass

            if token in Other:
                is_classified = True
                count['Other'] += 1
                try:
                    unique['Other'].append(token)
                except:
                    pass

            if token in RegulatoryOperators:
                is_classified = True
                count['RegulatoryOperators'] += 1
                try:
                    unique['RegulatoryOperators'].append(token)
                except:
                    pass

            if token in TaxOperands:
                is_classified = True
                count['TaxOperands'] += 1
                try:
                    unique['TaxOperands'].append(token)
                except:
                    pass

            total_words += 1
            if is_classified:
                total_classified += 1
            else: # add to list of unclassified words
                unique['unclassified'].append(token)

    print("  TOTAL WORDS: " + str(total_words))
    print("  TOTAL CLASSIFIED: " + str(total_classified))
    frac = float(total_classified)/float(total_words)
    print("  FRACTION CLASSIFIED: " + str(round(frac,2)))

    # add output
    out_text += input_file_name
    for count_key in sorted(count.keys()):
        out_text += ";" + str(count[count_key]) + ";" + str(len(set(unique[count_key])))

    #
    # compute num operators, operands
    #
    num_unique_operators = len(set(unique['RegulatoryOperators'])) + len(set(unique['LogicalConnectors']))
    num_unique_operands = len(set(unique['EconomicOperands'])) + len(set(unique['Attributes'])) + len(set(unique['LegalReferences'])) +  len(set(unique['TaxOperands']))
    num_operators = count['RegulatoryOperators'] + count['LogicalConnectors']
    num_operands = count['EconomicOperands'] + count['Attributes'] + count['LegalReferences'] + count['TaxOperands']

    total_volume = num_operators + num_operands
    potential_volume = 2.0 + num_unique_operands
    level = float(potential_volume) / float(total_volume)
    if True:
        print("    << TOTAL VOLUME:" + str(total_volume))
        print("    << POTENTIAL VOLUME:" + str(potential_volume))
        print("    << LEVEL:" + str(level))

    out_text += str(num_operators) + ";" + str(num_operands) + ";" + str(num_unique_operators) + ";" + str(num_unique_operands) + ";"
    out_text += str(total_volume) + ";" + str(potential_volume) + ";" + str(level) + "\n"

    #
    # write results file
    #
    out_file = open("results-" + output_file_name, 'w')
    out_file.write(out_text)
    out_file.close()
    print("   RESULTS WRITTEN TO: " + "results-" + output_file_name)

    #
    # write out unclassified tokens
    #
    out_text = ""
    out_file = open("unclassified-" + output_file_name, "w")
    for token in set(unique['unclassified']):
        out_text += token + ";" + str(unique['unclassified'].count(token)) + "\n"
    out_file.write(out_text)
    out_file.close()
    print("   UNCLASSIFIED TOKENS WRITTEN TO: " + "unclassified-" + output_file_name)

    #
    # write frequency file
    #
    out_text = ""
    out_file = open("frequency-" + output_file_name, 'w')
    for token in set(unique['RegulatoryOperators']):
        out_text += "RegulatoryOperators;" + token + ";" + str(unique['RegulatoryOperators'].count(token)) + "\n"
    for token in set(unique['LogicalConnectors']):
        out_text += "LogicalConnectors;" + token + ";" + str(unique['LogicalConnectors'].count(token)) + "\n"
    for token in set(unique['EconomicOperands']):
        out_text += "EconomicOperands;" + token + ";" + str(unique['EconomicOperands'].count(token)) + "\n"
    for token in set(unique['Attributes']):
        out_text += "Attributes;" + token + ";" + str(unique['Attributes'].count(token)) + "\n"
    for token in set(unique['LegalReferences']):
        out_text += "LegalReferences;" + token + ";" + str(unique['LegalReferences'].count(token)) + "\n"
    for token in set(unique['TaxOperands']):
        out_text += "TaxOperands;" + token + ";" + str(unique['TaxOperands'].count(token)) + "\n"
    out_file.write(out_text)
    out_file.close()
    print("   FREQUENCIES WRITTEN TO: " + "frequency-" + output_file_name)

    #
    # END
    #
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
