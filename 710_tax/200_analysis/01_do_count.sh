#!/bin/bash
# Prepare glossary
# ./05_prepare_glossary.py ../020_word_lists/RegulatoryOperators_Tax-raw.txt ../020_word_lists/RegulatoryOperators_Tax-clean.txt

# ANALYZE TEXT
for entry in Pillar1 Pillar2 OECD OECD_NoGlossary UN UN_NoGlossary UN_NoGlossary_NoCountry ;
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done

# for entry in OECD Pillar1_ProfitSplit-Sections OECD_ProfitSplit-Sections UN_ProfitSplit-Sections ;
#   do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
# done
# for entry in OECD_DisputeSettlement-Sections Pillar1_DisputeSettlement-Sections;
#   do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
# done

rm results/results.csv 2>/dev/null
cat results/results*.csv >> results/results.csv

# # CREATE HISTOGRAMS
for entry in Pillar1 Pillar2 OECD OECD_NoGlossary UN UN_NoGlossary UN_NoGlossary_NoCountry Pillar1_ProfitSplit-Sections OECD_ProfitSplit-Sections UN_ProfitSplit-Sections OECD_DisputeSettlement-Sections Pillar1_DisputeSettlement-Sections;
  do ./11_create_histograms.py ./frequency/frequency-$entry.csv ./histograms/histo-$entry.csv ;
done
