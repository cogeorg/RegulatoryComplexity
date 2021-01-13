This directory contains the raw documents and code to replicate the results of Colliard, Eden, and Georg (2020), "Tax Complexity, Tax Certainty, and the OECD Pillar One And Two Blueprints
". The results for the paper are created using the shell script ./200_analysis/01_do_count.sh.

There are four subdirectories:
./010_raw_documents - Contains the raw documents used for our analysis. For the actual analysis we use the .txt files.
./020_word_lists - Contains the dictionary we use to classify words in the raw data. We distinguish between Operators, Operands, Other, and Unclassified. The last category is for words that can/should not be clearly classified into any of the other categories.
./200_analysis - Contains a number of scripts for our analysis.
- 10_do_analysis.py - The main file for our analysis. Reads the file to classify, as well as the dictionaries from ./020_word_lists and produces four outputs: a list of frequencies for each word in the dictionaries; a list of words that are not contained in the dictionaries, i.e. that cannot be classified; the result itself, containing the numbers required to compute the Halstead measures; and a histogram of frequencies.
- 11_create_histograms.py - A helper file used to create the histograms
- 12_check_duplicates.py - A helper file to check dictionary files for duplicates.
- 13_update_word_lists.py - A helper file to consolidate and update the dictionary files.
- 05_prepare_glossary.py - A helper file used in the creation of the tax-specific dictionaries.

Questions about the code can be sent to co-pierre.georg@uct.ac.za
