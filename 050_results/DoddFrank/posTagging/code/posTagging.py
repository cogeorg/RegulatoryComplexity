import re
import glob
from bs4 import BeautifulSoup


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

    paragraphs = []
    for par in text:
        par = re.sub("(U\.S\.C\.)", "U_S_C_", par)
        par = re.sub("(U\.S\.)", "U_S_", par)
        par = re.sub("(seq\.)", "seq_", par)
        par = re.sub("(App\.)", "App_", par)
        par = re.sub("(\.'')", "_''", par)
        sentences = par.split(".")
        sentences.pop()
        for s in sentences:
            s = s.strip()
            s = re.sub("_", ".", s)
            s = s + "."
            
            print s
            print "---"
        print "-----------------------"


'''
        sentences = par.split(".")
        sentences = ["auxiliarywordauxiliaryword"] + sentences
        sentences[-1] = "auxiliarywordauxiliaryword"

        trueSent = []
        aux = sentences[0]
        for i in range(1, len(sentences)-1):
            r = sentences[i-1]
            s = sentences[i]
            t = sentences[i+1]
            if len(s) < 13:
                aux = aux + "." + s
            else:
                if len(r) < 5:
                    aux = aux + "." + s
                    trueSent.append(aux)
                    aux = ""
                elif len(t) < 13:
                    aux = s
                else:
                    trueSent.append(s)
                    aux = ""
        

        for thing in trueSent:
            print thing
            print "------------------------------"

'''
