import re
import glob
from bs4 import BeautifulSoup
import subprocess
import os
import argparse
#from nltk.tag import StanfordPOSTagger


'''
# POS tagger
stanford_dir = '/home/sabine/Dokumente/Uni/Master/Masterarbeit/stanford-postagger-2015-12-09/'
modelfile = stanford_dir + 'models/english-bidirectional-distsim.tagger'
jarfile = stanford_dir + 'stanford-postagger.jar'
st = StanfordPOSTagger(model_filename=modelfile, path_to_jar=jarfile)
'''

def main(argv):
    cwd = os.getcwd()
    documents = []
    fileNames = []
    for f in os.listdir(cwd + argv.input):
        if f.endswith(".html"):

            # save name
            fileName = re.findall("(.*?)\.", f)[0]
            fileNames.append(fileName)

            data = ""
            # open files in designated folder
            with open (cwd + argv.input + '/' + f, "r") as myfile:
                for line in myfile:
                    line = line.replace('\n', '')
                    data += line

            # find all paragraphs
            pars = re.findall("(<div\sclass\s=\s\"ex5\">.*?</div>)", data)

            # save paragraphs withouth headlines
            text = []
            for par in pars:
                par = re.sub('>"\(.+?\)\s<span\s.*?\.</span>', '>', par)
                par = re.sub('>\(.+?\)\s<span\s.*?\.</span>', '>', par)
                par = re.sub('>"SEC\.\s[0-9]{3}\.\s[A-Z].*?\.', '>', par)
                #print par
                soup = BeautifulSoup(par)
                plain = soup.text
                plain = plain.strip()
                # replace non-ascii characters with whitespace
                plain = plain.encode('ascii', errors = 'ignore')
                text.append(plain)
                #print plain
                #print "------------------"

            #list of known abbreviations and their replacements
            abbrev = [r'(seq\.)', r'(App\.)', r'\."\.\(', r'(\.")']
            repl = ['seq_', 'App_', r'_"_\()', '_"']
            # capitalized abbreviations
            abbrevCap = re.findall('(\s[A-Z]\.([A-Z]\.){1,10})', data)
            for l in abbrevCap:
                a = l[0]
                a = a.strip()
                if a not in abbrev:
                    abbrev.append(a)
                r = a.replace('.', '_')
                if r not in repl:
                    repl.append(r)

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
                    if re.findall(r'following:\s*"\(.+?\)\s[A-Z]|following:\s*"[A-Z]|following:\s*[A-Z]', t):
                        s = t.split(":")
                        for i in s:
                            sent.append(i)
                    elif re.findall(r'section:\s*"\(.+?\)\s[A-Z]|section:\s*"[A-Z]|section:\s*[A-Z]', t):
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
                    s = re.sub(r'"', "", s)
                    s = s.strip()
                    # change number format
                    s = re.sub(r"(\$)([0-9]+),([0-9]+)", r"USD\2\3", s)
                    for i in range(3):
                        s = re.sub(r"(USD[0-9]+),([0-9]+)", r"\1\2", s)
                    # delete double period
                    s = re.sub(r"\.\.", ".", s)
                    if len(s) > 5:
                        sentences.append(s)
                        #print s
                        #print "-----------------"
                paragraphs.append(sentences)
            documents.append(paragraphs)

    '''
    pos = st.tag(test.split())
    print pos
    '''

    # Parsey McParseface to obtain POS and dependency tags
    os.chdir(cwd + argv.parser)

    docParse = []
    for doc in documents:
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
        docParse.append(parParse)

    os.chdir(cwd + argv.output)

    # save output as txt-file
    for doc in docParse:
        fileName = fileNames[docParse.index(doc)]
        with open(fileName + '.txt','w') as f:
            for par in doc:
                for sen in par:
                    for word in sen:
                        for item in word:
                            f.write("%s\t" %item)
                        f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-p', '--parser', help='Parser Directory', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
