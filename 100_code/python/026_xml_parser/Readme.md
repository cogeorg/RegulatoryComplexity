# Dodd-Frank xml Parser

Python code to buil the xml file for the Dodd-Frank document. The xml tree has the following structure:

xml document | Dodd-Frank document | 
------------ | ------------- | 
Titles | TITLE I-- <font color='red'>T</font>itle name  | 
Subtitle* | Subtitle A--<font color='red'>S</font>ubtitle name   | 
Part* |  PART I--<font color='red'>P</font>art name|   
Section | SEC. 1--<font color='red'>S</font>ection name | 
Paragraph | a) <font color='red'>P</font>aragraph name <font color='red'>--</font> | 
Bullet | (1) <font color='red'>B</font>ullet name <font color='red'>--</font>  | 
sub_bullet | (A) text   | 
third_bullet | (i) text  | 

NOTES:  
* Optional  

  

Shell (Runs the main python file)
 **RegulatoryComplexity/100_code/shells/003_parser_xml.sh**  
 note: *Change working directory (RegulatoryComplexity) at the top of the shell* 

Input (Dodd-Frank regulatory document)
 **RegulatoryComplexity/001_raw_data/html/dodd_frank.html**

Output (Dodd-Frank xml document)
 **RegulatoryComplexity/010_cleaned_data/** -> dodd_frank.xml

### Files
**RegulatoryComplexity/100_code/python/xml**  
1) tree.py  
2) dodd_frank.py   
3) xml_parser.py (main)

**RegulatoryComplexity/100_code/shell**  
4) 003_parser_xml.sh 

### Functions  
1) tree.py: Functions to build the xml tree. Each function buid a child node which represents the item of the document.

	1.1) build_title  
	1.2) build_section  
	1.3) build_subtitle  
	1.4) build_part  
	1.5) build_paragraph  
	1.6) build_bullet  
	1.7) build_subbullet  
	1.8) build_third_bullet  
	
	**args**  
    line_list (string list): The list of lines in the 	input text.  
    node (object): Parent node in the tree structure. 
     
    **rerturns**  
    node: Object with the information of the tree level 	and lower levels.

2) dodd_frank.py:  Functions to find the items of the documents  

    2.0) get_line_list  
    
    **args**   
    file_name (string): The directory of the file 
     
    **rerturns**      
    lines_list (string list): List of lines  
   
	2.1) find_title  
	2.2) find_section  
	2.3) find_subtitle   
	2.4) find_part  
	2.5) find_paragraph    
	2.6) find_bullet  
	2.7) find_sub_bullet  
	2.8) find_third_bullet  
	  
	**args**  
    lines_section (string): The cleaned list of lines from get_line_list.  
    **returns**  
    
    names(string): List of the names.  
    lines_section(List of List): Nested lists of lines for each item
    
	2.9) check_number  
	2.10) check_paragraph  
	2.11) check_sequence   
	2.12) check_upper 
	2.13) check_sequence_numbers
	2.14) check_proper_upper
	2.15) check_proper_upper
	  
	**args**  
    lines (string): line of text
      
    **returns**  
    True/False  
