import re
import glob
from bs4 import BeautifulSoup
#from bllipparser import RerankingParser
import subprocess
import os
#from nltk.tag import StanfordPOSTagger

# parser model
#rrp = RerankingParser.fetch_and_load('WSJ+Gigaword-v2', verbose=True)

'''
# POS tagger
stanford_dir = '/home/sabine/Dokumente/Uni/Master/Masterarbeit/stanford-postagger-2015-12-09/'
modelfile = stanford_dir + 'models/english-bidirectional-distsim.tagger'
jarfile = stanford_dir + 'stanford-postagger.jar'
st = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)
'''

documents = []
for f in glob.glob("*.html"):

    # open files in designated folder
    with open (f, "r") as myfile:
        data = myfile.read()
    
    # find all paragraphs
    pars = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)

    # save paragraphs withouth headlines
    text = []
    for par in pars:
        par = re.sub("\s\(.\)\s<span\s.*?\.--</span>", "", par)
        par = re.sub("``\(.\)\s<span\s.*?\.--</span>", "", par)
        soup = BeautifulSoup(par)
        plain = soup.text
        plain = plain.strip()
        text.append(plain)
        #print plain

    #list of known abbreviations and their replacements
    abbrev = [r"(U\.S\.C\.)", r"(U\.S\.)", r"(seq\.)", r"(App\.)", r"(\.'')"]
    repl = ["U_S_C_", "U_S_", "seq_", "App_", "_''"]
    #split paragraphs into sentences
    paragraphs = []
    for par in text:
        for a in abbrev:
            par = re.sub(a, repl[abbrev.index(a)], par)
        # split on .
        sen = par.split(".")
        # split on :
        sent = []
        for t in sen:
            s = t.split(":")
            for i in s:
                sent.append(i)
        sent.pop()
        sentences = []
        for s in sent:
            s = s.strip()
            s = re.sub("_", ".", s)
            s = s + "."
            s = str(s)
            sentences.append(s)
        paragraphs.append(sentences)
    documents.append(paragraphs)


'''
pos = st.tag(test.split()) 
print pos
'''

# Parsey McParseface to obtain POS and dependency tags
os.chdir('/home/sabine/Dokumente/Git/models/syntaxnet')


#trial: 3rd sentence in first paragraph
'''
sen = documents[0][0][2]
parse = subprocess.check_output('echo "%s" | syntaxnet/demo.sh' %sen, shell = True)
print parse

# convert output into list of 4 (word, universal tag, language specific tag, universal dependency relation)
rawParse = []
parseSplit = parse.split("\n")
for item in parseSplit:
    if len(item) < 2: continue
    else:
        raw = item.split("\t")
        raw = [raw[1], raw[3], raw[4], raw[7]]
        rawParse.append(raw)
'''

#docParse = []
#for doc in documents:
#    parParse = []
#    for par in doc:

doc = documents[0]
parParse = []
for par in doc:
    senParse = []
    for sen in par:
        parse = subprocess.check_output('echo "%s" | syntaxnet/demo.sh' %sen, shell = True)
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

for item in parParse:
    print item
    print "-----------------"
