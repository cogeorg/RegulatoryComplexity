#!/bin/bash

#cd /Users/alilimon/Documents/Research/ &&
cd /home/sabine/Dokumente/Git/ &&

python ./RegulatoryComplexity/100_code/python/040_legal_references/legal_references.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -o  ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/

python ./RegulatoryComplexity/100_code/python/040_legal_references/legal_references_inside.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -o  ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/
