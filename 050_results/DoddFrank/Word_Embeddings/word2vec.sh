#!/bin/bash

#cd /Users/co/git/
cd /home/sabine/Dokumente/Git/ &&

# # DFA
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/prepDFA.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/Original/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/ -m average -t Title -s 0 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/DFA/

# # Bible
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/prepBible.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/ -t Book -s 1 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Bible/

# # KWG
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/prepKWG.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/ -t Title -s 1 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWG/

# # KWG English
# ###############################################################################
# # preprocessing
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/prepKWGengl.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/
# # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/ -t Title -s 1 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/KWGengl/

# Alice
# ###############################################################################
# preprocessing
 python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Alice/prepAlice.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Alice/ -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Alice/
 # model
python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Alice/ -m tfidf -t Alice -s 1 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Alice/

# # Reuters Articles
# # ###############################################################################
# # preprocessing
#  python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Reuters/prepReuters.py -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Reuters/
#  # model
# python ./RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/word2vec2dist.py -i /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Reuters/ -t Category -s 1 -o /RegulatoryComplexity/050_results/DoddFrank/Word_Embeddings/Reuters/
