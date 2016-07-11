# Dodd-Frank html Visualizator

Python code to buil the html visualizator for the Dodd-Frank document.
  
Shell (Runs the main python file)
 **RegulatoryComplexity/100_code/shells/004_create_visuals.sh**  
note: *Change working directory (RegulatoryComplexity) at the top of the shell* 
 
Input (Dodd-Frank regulatory document)
 **RegulatoryComplexity/010_cleaned_data/dodd_frank.xml**

Output (Dodd-Frank xml document)
 **RegulatoryComplexity/050_results/DoddFrank/Visuals/** -> dodd_frank.html
  
### Python Files
**RegulatoryComplexity/100_code/python/030_create_visuals/create_visuals.py**    
1) create_visuals.py  
 
### Functions  
Not yet specified. 
 
### Additonal Files for the html visualiztion.
**RegulatoryComplexity/050_results/DoddFrank/Visuals/Templates/V1_visualizator**  
 1) dodd_frank.html: preview of the dodd_frank.html with highlighted words. 
 
**RegulatoryComplexity/050_results/DoddFrank/Visuals/Templates/V1_visualizator/Style_Files**  
1) style_sheet.css: Format sheet for the HTML  
2) javascript.js:  Java function to highlight the words with a click.  
3) light_files and result_files (Folder): JQuery packages used in the html visualizator. 





