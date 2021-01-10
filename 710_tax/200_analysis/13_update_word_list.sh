#!/bin/bash

./13_update_word_lists.py OPERANDS ../020_word_lists/Operands.txt FREQUENCY-4TEXTS_jec.csv
./13_update_word_lists.py OPERATORS ../020_word_lists/Operators.txt FREQUENCY-4TEXTS_jec.csv
./13_update_word_lists.py OTHER ../020_word_lists/Other.txt FREQUENCY-4TEXTS_jec.csv
./13_update_word_lists.py UNCLASSIFIED ../020_word_lists/Unclassified.txt FREQUENCY-4TEXTS_jec.csv
