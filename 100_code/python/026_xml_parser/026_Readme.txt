Dodd-Frank Xlm Parser

Python program to make the xlm file for the Dodd Frank document. 

Shell 
RegulatoryComplexity/100_code/shells/003_parser_xml.sh
—Runs the main file of python-

Input
001_raw_data/htm/Dodd_Frank.htm

Output
010_cleaned_data/Dodd_Frank.xlm

Files
1) tree.py		——Python——
2) dodd_frank.py 	——Python——
3) xlm_parser (main)	——Python——
4) 003_parser_xml	——Shell——

Functions
1) tree: Functions to build the xlm tree 

	Main Functions.-
	
	1.1) build_title()
	1.2) build_section()
	1.3) build_subtitle()
	1.4) build_part()
	1.5) build_paragraph()
	1.6) build_bullet()
	1.7) build_subbullet()
	1.8) build_third_bullet()

2) dodd_frank: Functions to find the titles, sections, paragraphs, …
	
	Main Functions.-	

	2.0) get_line_list()
	2.1) find_title()
	2.2) find_section()
	2.3) find_subtitle()
	2.4) find_part()
	2.5) find_paragraph()

	Others.-
	2.6) check_number()
	2.7) check_paragraph()
	2.8) check_sequence() 
	2.9) check_upper()
	2.10) check_sequence_numbers

3) xlm_parser: Main 

