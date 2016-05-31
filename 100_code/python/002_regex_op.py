import re
import pandas as pd
import numpy as np

#Function to get different features od the text
def bullet_levels(text):
    # First level bullet
    regex=  r"\([a-z]\)\s[A-Z]+[\,\sA-Z]*"
    bullet_1l = re.findall(regex, text[0])

    # Second level bullet
    regex=  r"\([0-9]\)\s[A-Z]+[\,\sA-Z]*"
    bullet_2l = re.findall(regex, text[0])

    # Third level bullet
    regex=  r"\([A-Z]\)\s[A-Z]+[\,\sA-Z]*"
    bullet_3l = re.findall(regex, text[0])
    return len(bullet_1l), len(bullet_2l), len(bullet_3l)

def referencesSec(text):
#References to subsections subparagraph, paragraph or sections ...
    regex="subparagraph \(| subparagraphs \(| paragraph \(| paragraphs \(| subsection \(|  subsections \( "
    references = re.findall(regex, text[0])
    return len(references)


def definition(text):
    regex=r"mean\s| mean\,| Mean\s| Mean\, "
    def_1 = re.findall(regex, text[0])

    regex=r"means\s| means\,| Means\s| Means\,"
    def_2 = re.findall(regex, text[0])

    regex=r"meaning\s| meanings\s"
    def_3 = re.findall(regex, text[0])
    return len(def_1), len(def_2), len(def_3) 


def condTerms(text):
    regex=r"if| except| but| provided| when| where| whenever| unless| notwithstanding| in no event| and in the event"
    terms=re.findall(regex, text[0])
    return len(terms)


file_name = "010_cleaned_data/DODDFRANK.txt"
f = open(file_name)
lines = f.read()


#Titles of DoddFrank document
regex=  r"TITLE\s*[V,I,X]+[\sA-Z]+"
title = re.findall(regex, lines)

bullets_1=[]
bullets_2=[]
bullets_3=[]
referencesP=[]
def_1=[]
def_2=[]
def_3=[]
cond_Terms=[]

for i in range(len(title)-1):
    #Split the text by title 
    my_regex = re.escape(title[i]) + r".*?"+re.escape(title[i+1])
    text=re.findall(my_regex,lines)
    aux_fun=bullet_levels(text)
    bullets_1.append(aux_fun[0])
    bullets_2.append(aux_fun[1])
    bullets_3.append(aux_fun[2])
    referencesP.append(referencesSec(text))
    aux_fun=definition(text)
    def_1.append(aux_fun[0])
    def_2.append(aux_fun[1])
    def_3.append(aux_fun[2])
    cond_Terms.append(condTerms(text))


