Dodd Frank visualizer 
=========

Running
-------

To run the application in the development web server just execute `run.py` (python run.py in terminal). Then, open `http://localhost:5000/` in the browser. 


Features
-------
 
1) Highlighting of selected text: Select and pick the color for each word(s).    

2) Update and find the list of words: Update the list of words highlighted during your session and find them in the document. Depending on how common is the word(s) the task can take different times.

3) Remove words: Select and remove words already highlighted.   
  
 
Output file
------- 
Check your current list of words `app/output/output.csv`.  
**Note: Words prevously classified (master files) are shown by default in the document view**

How it works?
-------
1) Select the word.  
2) Right click.   
3) Choose the type of word or the task.
  

**Bug: You must open the right-click menu every time you select a word. Otherwise, the highlighter is applied to all the words you selected since the last right-click. If two words are highlighted, you just need to re-highlight the wrong word. **


 



