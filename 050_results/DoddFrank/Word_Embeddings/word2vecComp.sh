#!/bin/bash

#cd /Users/co/git/
cd /home/sabine/Dokumente/Git/ &&

# Alice vs. DFA
###############################################################################
#python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vecComp.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/ -l Alice DFA -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA_Alice/

# DFA vs. KWG
###############################################################################
python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vecComp.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/ -l DFA KWGengl -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA_KWG/
