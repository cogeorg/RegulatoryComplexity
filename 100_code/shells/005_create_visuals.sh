#!/bin/bash

cd /home/sabine/Dokumente/Git &&
#cd /Users/co/git/

python ./RegulatoryComplexity/100_code/python/030_create_visuals/create_visuals.py -i ./RegulatoryComplexity/010_cleaned_data/Dodd_Frank.xml -w ./RegulatoryComplexity/020_auxiliary_data/Sections/Protected_list/ -o ./RegulatoryComplexity/050_results/DoddFrank/Visuals/DF_Templates_Protected/
