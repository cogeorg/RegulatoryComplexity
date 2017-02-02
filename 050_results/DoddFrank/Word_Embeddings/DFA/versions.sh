#!/bin/bash

#cd /Users/co/git/
cd /home/sabine/Dokumente/Git/ &&

# preprocess individual versions of DFA
# for f in ./RegulatoryComplexity/001_raw_data/xml/*
# do
#     file=${f##*/}
#     filename=${file%.*}
#
#     python ./RegulatoryComplexity/100_code/python/031_parser_visualizer/xml2html.py -i  $f -t sentences -o  ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/Original/
#     #
#     python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prepDFA.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/Original/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prep/$filename/
# done

python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/word2vecComp.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prep/ -t Title -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/output/
