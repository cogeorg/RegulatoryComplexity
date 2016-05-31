import re
import pandas as pd
#Read file 
file_name = "001_raw_data/txt/DODDFRANK.txt"
f = open(file_name)
#Preprocessing of the data 
#Delete index
lines = f.read().decode('utf-8')
lines=re.sub(u'\2013|\u2014|\u2018|\u2019|\n',' ',lines, flags=re.DOTALL)
lines= re.findall(r'(?:SEC. 2. DEFINITIONS)(.*)',lines)
lines = "SEC. 2. DEFINITIONS" + lines[0]
#Cleaning text
lines= re.sub('VerDate Nov 24 2008','',lines)
lines= re.sub('00:54 Jul 29, 2010','', lines)
#Save text
file_name="010_cleaned_data/DODDFRANK.txt"
f = open(file_name, 'w')
f.write(lines.encode('utf8'))
f.close()
