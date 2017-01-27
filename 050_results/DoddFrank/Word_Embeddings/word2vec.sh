#!/bin/bash

#cd /Users/co/git/
cd /home/sabine/Dokumente/Git/ &&

# # DFA
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prepDFA.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/Original/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/ -t Title -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/

# # Bible
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/prepBible.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/ -t Book -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/

# KWG
###############################################################################
# preprocessing
#python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/prepKWG.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/
# model
#python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/ -t Title -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/

# # KWG English
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/prepKWGengl.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -t Title -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/

# DFA vs. KWG English
###############################################################################
# preprocessing
python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prepDFA.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/Original/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/
python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/prepKWGengl.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/
# model
python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vecComp.py -ia /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/ -ix /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -t Title -oa /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/ -ox /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/
