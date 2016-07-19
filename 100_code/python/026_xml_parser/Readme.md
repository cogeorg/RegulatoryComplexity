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
two_bullet | (A) text   | 
three_bullet | (i) text  | 
four_bullet | (I) text  | 
five_bullet | (aa) text  | 
six_bullet | (AA) text  | 
Section (Amended)| ``SEC.  |
Paragraph/ bullet/... (Amended)| ``([A-Z0-9])  |


NOTES:  
* Optional  

  




Shell (Runs the main python file)
 **RegulatoryComplexity/100_code/shells/003_parser_xml.sh**

Input (Dodd-Frank regulatory document)
 **/RegulatoryComplexity/001_raw_data/html/dodd_frank.html**

Output (Dodd-Frank xml document)
 **Research/RegulatoryComplexity/010_cleaned_data/** -> dodd_frank.xml

### Python Files
**/RegulatoryComplexity/100_code/python/026_xml_parser/**  
1) tree.py  
2) dodd_frank.py   
3) checkers.py  
4) item_functions.py   
5) xml_parser.py (main)


### Functions  
1) tree.py: Functions to build the xml tree. Each function buid a child node which represents the item of the document.

	1.1) build_item  
	1.2) build_amended_item 

	
	**args**  
    line_list (string list): The list of lines in the input text.  
    node (object): Parent node in the tree structure. 
    is_amended (boolean): True if the item is an amended section.  
    item_type (string): Type of the item.   
     
    **rerturns**  
    element_not_empty: True if an item node was built

2) dodd_frank.py:  Functions to find the items of the documents  

    2.0) get_line_list  
    
    **args**   
    file_name (string): The directory of the file 
     
    **rerturns**      
    lines_list (string list): List of lines  
   
	2.1) find_item 
	  
	**args**  
    lines_list (string list): The cleaned list of lines from get_line_list.  
    is_amended (boolean): True if you are looking for amended types/ False otherwise.  
    item_type (string): Name of the item type that you want to find.  
    
    **returns**  
    
     names: List of item's names.
     lines_section: List of lists. Each nested list is linked to each item.  
     
3) checkers.py:  Functions to identify if a line is an item.       
    
	3.0) check_number  
	3.1) check_paragraph  
	3.2) check_upper  
	3.3) check_three_clause 
	3.4) check_four_clause
	3.5) check_five_clause
	3.6) check_six_clause 
	  
	**args**  
    lines (string): line of text
      
    **returns**  
    True/False  
    
    3.7) check_sequence_paragraph
    3.8) check_sequence_number
    3.9) check_sequence_upper 
    3.10) check_sequence_clause
    
    **args**  
    word/number, names, is_amended  (string, string list, boolean)
      
    **returns**  
    True/False  
    
    
     3.11) check_h_i 
     3.12) check_same_sentence, 
     3.13) check_sub_part
     3.14) check_nothing
	 3.15) format_line
	 3.16) get_item 
	 3.17) clean_note 
	 
	 
4) item_functions.py:  Functions that join the checker functions depending of the item_type. 

	4.0) is_title  
	4.1) is_part  
	4.2) is_subtitle  
	4.3) is_section
	4.4) is_paragraph
	4.5) is_bullet
	4.6) is_two_bullet 
	4.7) is_three_bullet
	4.8) is_four_bullet
	4.9) is_six_bullet
	4.10) is_part_sec_sub
	4.11) is_par_num
	  
	**args**  
    line , names (opt), is_amended(opt), list_aux (opt) (string, string list, boolena, list of list)
      
    **returns**  
    True/False  
    
    4.12) get_amended_item
    4.13) get_list_levels
    4.14) get_checker_functions
    
   	**args**  
    item (string)
      
    **returns**  
     list (string list/ function list) 



	 
	 
	 
    
