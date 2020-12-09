#!/bin/bash
# Prepare glossary
# ./05_prepare_glossary.py ../020_word_lists/RegulatoryOperators_Tax-raw.txt ../020_word_lists/RegulatoryOperators_Tax-clean.txt

# Then do analysis
for entry in Pillar1 Pillar2 OECD OECD_NoGlossary UN_NoGlossary UN_NoGlossary_NoCountry UN_NoCountry;
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done
#
# wait 10

for entry in OECD_ProfitSplit-Sections
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done
for entry in Pillar1_ProfitSplit-Sections UN_ProfitSplit-Sections OECD_DisputeSettlement-Sections Pillar1_DisputeSettlement-Sections;
  do time ./10_do_analysis.py ../010_raw_documents/$entry.txt $entry.csv;
done

rm results.csv 2>/dev/null
cat results*.csv >> results.csv
