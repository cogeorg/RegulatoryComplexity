#!/bin/bash

cp ~/git/RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/PreClass/* html/
./10_do_analysis.py html/ 50_results/word_count.csv
