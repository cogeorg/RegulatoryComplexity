import re
from bs4 import BeautifulSoup
import os
import pickle
import argparse


# prepocessing
################################################################################
def main(argv):
    cwd = os.getcwd()
    titles = []
    for f in os.listdir(cwd + argv.input):
        if f.endswith(".html"):

            # save name
            titleName = re.findall("(.*?)\.", f)[0]
            titleNum = int(titleName.split('_')[1])

            data = ""
            # open files in designated folder
            with open (cwd + argv.input + '/' + f, "r") as myfile:
                for line in myfile:
                    line = line.replace('\n', '')
                    data += line

            # find all sections
            section = re.findall(r'SEC\..*?ex4|SEC\..*?/body', data)

            sections = []
            for sec in section:

                # find all paragraphs
                pars = re.findall("(<div\sclass\s=\s\"ex5\">.*?</div>)", sec)

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
                        if re.findall(r'following:\s*"\(.+?\)\s[A-Z]|following:\s*"[A-Z]|following:\s*[A-Z]|following:\s\([0-9]+\)', t):
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

                    # split in words
                    sents = []
                    for s in sentences:
                        words = s.split()
                        sents.append(words)


                    # strip punctuation
                    sentences = []
                    for s in sents:
                        words = []
                        for c, w in enumerate(s, start=1):
                            w = w.strip(',')
                            w = w.strip(';')
                            w = w.strip(':')
                            if c == len(s):
                                w = w.strip('.')
                            w = w.strip('"')
                            w = w.lower()
                            words.append(w)
                        sentences.append(words)

                    # U.S.C. references as 1 word
                    flag = 0
                    ref = ""
                    left = 0
                    right = 0
                    sents=[]
                    for s in sentences:
                        words = []
                        for w in s:
                            if flag == 0:
                                if not w.startswith('('):
                                    words.append(w)
                                elif (w.startswith('(')) and (')' in w):
                                    words.append(w)
                                elif (w.startswith('(')) and (not w[-1].isdigit()):
                                    words.append(w)
                                else:
                                    ref += w + ' '
                                    left += w.count('(')
                                    flag = 1
                            else:
                                right += w.count(')')
                                left += w.count('(')
                                if left == right:
                                    ref += w
                                    words.append(ref)
                                    flag = 0
                                    right = 0
                                    left = 0
                                    ref=""
                                else:
                                    ref += w + ' '
                        sents.append(words)

                    # strip parentheses
                    sentences = []
                    for s in sents:
                        words = []
                        for w in s:
                            if ('(' in w) and (')' not in w):
                                w = w.strip('(')
                            elif ('(' not in w) and (')' in w):
                                w = w.strip(')')
                            words.append(w)
                        sentences.append(words)
                        #print words
                        #print '-----------------'
                    paragraphs.append(sentences)
                sections.append(paragraphs)
        titles.append([titleNum, sections])

    # sort titles
    titles = sorted(titles)

    # create datasets
    pythonData = []
    modelData = []
    for t in titles:
        title = []
        for sec in t[1]:
            section = []
            for p in sec:
                for s in p:
                    section.append(s)
                    modelData.append(s)
            title.append(section)
        pythonData.append(title)

    # save datasets
    with open(cwd + argv.output + 'pythonData', 'w') as f:
        pickle.dump(pythonData, f)
    with open(cwd + argv.output + 'modelData', 'w') as g:
        pickle.dump(modelData, g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
