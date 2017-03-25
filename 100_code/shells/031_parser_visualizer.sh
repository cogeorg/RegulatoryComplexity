#!/bin/bash

cd /Users/co/git/
#cd /home/sabine/Dokumente/Git/ &&

# Words Version without preclassification
#python ./RegulatoryComplexity/100_code/python/031_parser_visualizer/xml2html.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -t words -o  ./RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/Original/

# Words Version with preclassification
python ./RegulatoryComplexity/100_code/python/031_parser_visualizer/xml2html.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -t words -w ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/ -o  ./RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/PreClass/

# Sentence Version
#python ./RegulatoryComplexity/100_code/python/031_parser_visualizer/xml2html.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -t sentences -o  ./RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/sentences/templates/Original/

# Coherence Version with preclassification
#python ./RegulatoryComplexity/100_code/python/031_parser_visualizer/xml2html.py -i  ./RegulatoryComplexity/001_raw_data/xml/DFA.xml -t coherence -w ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/coherence/ -o  ./RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/coherence/templates/PreClass/
