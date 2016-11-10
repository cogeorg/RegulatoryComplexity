import re
import glob
from bs4 import BeautifulSoup
import subprocess
import os
#from nltk.tag import StanfordPOSTagger


'''
# POS tagger
stanford_dir = '/home/sabine/Dokumente/Uni/Master/Masterarbeit/stanford-postagger-2015-12-09/'
modelfile = stanford_dir + 'models/english-bidirectional-distsim.tagger'
jarfile = stanford_dir + 'stanford-postagger.jar'
st = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)
'''

documents = []
for f in glob.glob("*.html"):

    # save name
    fileName = re.findall("(.*?)\.", f)[0]

    # open files in designated folder
    with open (f, "r") as myfile:
        data = myfile.read()

    # find all paragraphs
    pars = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)

    # save paragraphs withouth headlines
    text = []
    for par in pars:
        par = re.sub(">``\(.+?\)\s<span\s.*?\.--</span>", ">", par)
        par = re.sub(">\(.+?\)\s<span\s.*?\.--</span>", ">", par)
        par = re.sub("\(.+?\)\s<span\s.*?\.--</span>", "", par)
        par = re.sub(">\s*\(.+?\)\s[A-Z].*--", ">", par)
        par = re.sub("``SEC\.\s[0-9]{3}\.\s[A-Z].*\.\s*<div\sclass=\"ex5\"> ", "", par)
        #print par
        soup = BeautifulSoup(par)
        plain = soup.text
        plain = plain.strip()
        text.append(plain)
        #print plain
        #print "------------------"

    #list of known abbreviations and their replacements
    abbrev = [r"(U\.S\.C\.)", r"(U\.S\.)", r"(seq\.)", r"(App\.)", r"C\.F\.R\.", r"\.''\.\(", r"(\.'')"]
    repl = ["U_S_C_", "U_S_", "seq_", "App_", "C_F_R_", r"_''_\()", "_''"]
    #split paragraphs into sentences
    paragraphs = []
    for par in text:
        # replace abbreviations
        for a in abbrev:
            par = re.sub(a, repl[abbrev.index(a)], par)
        # replace numbers /w dots
        par = re.sub(r"([0-9])\.([0-9])", r"\1_\2", par)
        # split on .
        sen = par.split(".")
        # split on :
        sent = []
        for t in sen:
            # some tags were not removed
            t = re.sub("/div>","",t)
            t = t.strip()
            # decide when to split after ":"
            if t.endswith(":"):
                s = re.sub(":$", ".", t)
                sent.append(s)
            if re.findall(r"following:\s*``\(.+?\)\s[A-Z]|following:\s*``[A-Z]|following:\s*[A-Z]", t):
                s = t.split(":")
                for i in s:
                    sent.append(i)
            elif re.findall(r"section:\s*``\(.+?\)\s[A-Z]|section:\s*``[A-Z]|section:\s*[A-Z]", t):
                s = t.split(":")
                for i in s:
                    sent.append(i)
            else:
                sent.append(t)
        sent.pop()
        sentences = []
        for s in sent:
            s = s.strip()
            # resubstitute period
            s = re.sub("_", ".", s)
            s = s + "."
            s = str(s)
            # delete quotes
            s = re.sub(r"`", "", s)
            s = re.sub(r"'", "", s)
            s = s.strip()
            # change number format
            s = re.sub(r"(\$)([0-9]+),([0-9]+)", r"USD\2\3", s)
            for i in range(3):
                s = re.sub(r"(USD[0-9]+),([0-9]+)", r"\1\2", s)
            # delete double period
            s = re.sub(r"\.\.", ".", s)
            #print s
            #print "-----------------"
            sentences.append(s)
        paragraphs.append(sentences)
    documents.append(paragraphs)

'''
pos = st.tag(test.split())
print pos
'''

# Parsey McParseface to obtain POS and dependency tags
os.chdir('/home/sabine/Dokumente/Git/models/syntaxnet')

#docParse = []
#for doc in documents:
#    parParse = []
#    for par in doc:

doc = documents[0]
parParse = []
for par in doc:
    senParse = []
    for sen in par:
        # dependency parsing
        parse = subprocess.check_output('echo "%s" | syntaxnet/demo.sh' %sen, shell = True)
        # convert output into list of 4 (word, universal tag, language specific tag, universal dependency relation)
        parseSplit = parse.split("\n")
        wordParse = []
        for item in parseSplit:
            if len(item) < 2: continue
            else:
                raw = item.split("\t")
                raw = [raw[1], raw[3], raw[4], raw[7]]
                wordParse.append(raw)
        senParse.append(wordParse)
    parParse.append(senParse)

os.chdir('/home/sabine/Dokumente/Git/RegulatoryComplexity/050_results/DoddFrank/110_posTagging/output')

# save output as txt-file
f = open(fileName + '.txt','w')
for par in parParse:
    for sen in par:
        for word in sen:
            for item in word:
                f.write("%s\t" %item)
            f.write("\n")
f.close()
