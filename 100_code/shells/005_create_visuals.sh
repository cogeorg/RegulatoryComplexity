#!/bin/bash

#cd /Users/alilimon/Documents/Research/ &&
#cd /Users/co/git/
cd /home/sabine/Dokumente/Git/ &&

python ./RegulatoryComplexity/100_code/python/030_create_visuals/create_visuals.py -i  ./RegulatoryComplexity/010_cleaned_data/dodd_frank.xml -w ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/ -o  ./RegulatoryComplexity/050_results/DoddFrank/Visuals/DF_Templates_Protected/

/bin/cp -rf ./RegulatoryComplexity/050_results/DoddFrank/Visuals/DF_Templates_Protected/* ./RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/PreClass
