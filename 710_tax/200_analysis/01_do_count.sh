#!/bin/bash
# Prepare glossary
# ./05_prepare_glossary.py ../020_word_lists/RegulatoryOperators_Tax-raw.txt ../020_word_lists/RegulatoryOperators_Tax-clean.txt

# Then do analysis
time ./10_do_analysis.py ../010_raw_documents/OECD.txt OECD.csv
time ./10_do_analysis.py ../010_raw_documents/UN.txt UN.csv

rm results.csv 2>/dev/null
cat *.csv >> results.csv
