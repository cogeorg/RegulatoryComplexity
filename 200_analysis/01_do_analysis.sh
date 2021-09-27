#!/bin/bash

# cp ~/git/RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/PreClass/* html/
# cp ~/git/RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/words/templates/Original/* html_noclass/
# cp ~/git/RegulatoryComplexity/010_cleaned_data/DODDFRANK.txt .

# ./10_do_analysis.py html/ 50_results/word_count.csv
# ./11_create_word_dictionary.py html/ 50_results/all_words_dictionary.csv

# ./12_count_txt.py ./txt/ ./50_results/all_words_dictionary_clean.csv ./50_results/txt/
# ./12_count_txt.py ./txt/ ./50_results/Master_clean.csv ./50_results/txt/

# ./12_count_html.py ./test/ ./50_results/test/
# ./12_count_html.py ./html/ ./50_results/html/
# cd 50_results/html/
# rm *_all_titles.* 2>/dev/null
# cat *.csv >> results_all_titles.csv
# cat *.txt >> residual_all_titles.txt
# cd ../../

# ./13_standardize_master.py ../020_auxiliary_data/Sections/Protected_list/Master_extended.csv ../020_auxiliary_data/Sections/Protected_list/Master_standardized.csv

# ./14_count_html_noclass.py ./html_noclass/ ../020_auxiliary_data/Sections/Protected_list/Master_consolidated.csv ./50_results/html_noclass/
