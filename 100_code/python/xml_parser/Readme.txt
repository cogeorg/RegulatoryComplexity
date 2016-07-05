Dodd-Frank Xlm Parser

Python program to make the xlm file for the Dodd Frank document. 

Input
001_raw_data/htm/Dodd_Frank.htm

Output
010_cleaned_data/Dodd_Frank.xlm

Files
1) tree
2) dodd_frank
3) xlm_parser (main)

Functions
1) tree: Functions to build the xlm tree 
	1.1) build_title()
	1.2) build_section()
	1.3) build_subtitle()
	1.4) build_part()
	1.5) build_paragraph()

Note 1: Need to add attributes to the node. 
Note 2: Need to add build_bullet(), build_subbullet().

2) dodd_frank: Functions to find the titles, sections, paragraphs, …
	
	2.0) get_line_list()
	2.1) find_title()
	2.2) find_section()
	2.3) find_subtitle()
	2.4) find_part()
	2.5) find_paragraph()

	Others) check_number(), check_paragraph(), check_sequence()

Note 1: Try to join the “find” functions. 

3) xlm_parser: Main 

