# RegulatoryComplexity
This is the code repository for the research project "Measuring Regulatory Complexity" by Jean-Edouard Colliard and Co-Pierre Georg. Use this code at your own risk. The code provides a simple dashboard that allows users to classify words in large regulatory texts (in our case the Dodd-Frank Act) in various categories, e.g. as operators or operands. This is useful when measuring the complexity of the regulatory text using the Halstead (1977) measures. Use at your own risk.

Source of raw data
https://www.fdic.gov/regulations/laws/important/

Pdf to txt
It will parse pdf documents located in 001_raw_data to txt.
Input:  001_raw_data/pdf/*.pdf
Run the shell 100_code/shells/001_totxt.sh
Output: 001_raw_data/txt/*.txt

Pdf to xlm (maximum 100 pages per document)
It will parse pdf documents located in 001_raw_data to xlm.
Input:  001_raw_data/pdf/*.pdf
Run the shell 100_code/shells/001_toxlm.sh
Output: 001_raw_data/xlm/*.xlm

Clean data for Dodd-Frank
Input:001_raw_data/txt/DODDFRANK.txt
Run 100_code/python/001_clean_data

Halstead Measures.

Features of the text such as bullets, definitions, references...
Input: 010_cleaned_data/DODDFRANK.txt
Run 100_code/python/002_regex_op

# Updated Analysis 2016-06-15
python 100_code/python/010_split_sections-DF.py 010_cleaned_data/DODDFRANK.txt 010_cleaned_data/DoddFrank/Sections/

