import re
import glob
import os
import argparse


for file in glob.glob("TITLE I--FINANCIAL STABILITY.html"):

    titles = ["TITLE I-", "TITLE II-", "TITLE III-", "TITLE IV-", "TITLE V-", 
                "TITLE VI-", "TITLE VII-", "TITLE VIII-", "TITLE IX-", "TITLE X-",
                "TITLE XI-", "TITLE XII-", "TITLE XIII-", "TITLE XIV-", "TITLE XV-",
                "TITLE XVI-"]
    newTitles = ["title_1", "title_2", "title_3", "title_4", "title_5", "title_6", 
                    "title_7", "title_8", "title_9", "title_10", "title_11", 
                    "title_12", "title_13", "title_14", "title_15", "title_16"]

    base = os.path.basename(file)

    for title in titles:
        if base.startswith(title):
            base = newTitles[titles.index(title)] + ".html"
        else: continue

    with open (file, "r") as myfile:
        data = myfile.read()

    
    replacement = re.findall("\)\s([A-Z].{1,100}?\.--)", data)
    uniqueReplacement = []
    for line in replacement:
        if line not in uniqueReplacement:
            uniqueReplacement.append(line)

    replacement = uniqueReplacement
    replacement.sort(key = len, reverse = True)


    # include spans for headlines
    for line in replacement:
        data = re.sub(line, "<span class=H>" + line +"</span>", data)

    #delete "--" 
    data = re.sub("([a-z])(--)", r'\1', data)

    # delete "\" around numbers
    data = re.sub(r"\\", "", data)

    f = open(base,'w')
    f.write(data)
    f.close()


