import lxml.etree as etree
import re
import os
import pickle
import argparse


# prepocessing
################################################################################
def main(argv):
    cwd = os.getcwd()
    parse = etree.parse(cwd + argv.input + 'KWG.xml')

    flag = 0
    titles = []
    title = []
    section = []
    paragraph = ''
    for action, elem in etree.iterwalk(parse, events=('start', 'end')):
        #print action, '|', elem.tag, '|', elem.text
        if action == "start":
            if flag == 0:
                if elem.tag == "Content":
                    flag = 1
            if flag == 1:
                if (elem.tag == "P") and (elem.text != None):
                    section.append(paragraph)
                    paragraph = elem.text + ' '
                elif (elem.tag == "DT") and (elem.text != None):
                    paragraph += elem.text + ' '
                elif elem.tag == "LA":
                    paragraph += elem.text + ' '
        if action == "end":
            if elem.tag == "Content":
                flag = 0
            elif (elem.tag == "gliederungsbez") and ('Abschnitt' in elem.text):
                section.append(paragraph)
                title.append(section)
                titles.append(title)
                title = []
                section = []
                paragraph = ''
            elif elem.tag == "gliederungstitel":
                section.append(paragraph)
                if len(section) > 1 or section[0] != '':
                    title.append(section)
                section = []
                paragraph = ''

    section.append(paragraph)
    title.append(section)
    titles.append(title)

    titles = titles[1:]

    abbrevs = ['a.', 'Abs.', 'b.', 'c.', 'Nr.', 'ABl.', 'S.', 'BGBl.', 'u.', 'vgl.', 'd.', 'Gem.', 'v.', 'e.', 'I.', 'bzw.']
    repl = ['a_', 'Abs_', 'b_', 'c_', 'Nr_', 'ABl_', 'S_', 'BGBl_', 'u_', 'vgl_', 'd_', 'Gem_', 'v_', 'e_', 'I_', 'bzw_']
    tits = []
    for t in titles:
        secs = []
        for sec in t:
            pars = []
            for p in sec:
                if p:
                    # replace "." after numbers
                    p = re.sub(r'([0-9]+)\.', r'\1_', p)
                    abs = re.findall(r'[A-Za-z]+\.', p)
                    # replace abbreviations
                    for i in range(len(abbrevs)):
                        p = p.replace(abbrevs[i], repl[i])
                    sentences = p.split('.')
                    sents = []
                    for s in sentences:
                        s = s.strip()
                        if s:
                            words = s.split(' ')
                            cleanWords = []
                            for w in words:
                                w = w.strip()
                                w = w.strip('_')
                                w = w.strip(':')
                                w = w.strip(';')
                                w = w.strip('(')
                                w = w.strip(')')
                                w = w.strip('[')
                                w = w.strip(']')
                                w = w.lower()
                                if w:
                                    cleanWords.append(w)
                            #print cleanWords
                            sents.append(cleanWords)
                    pars.append(sents)
            secs.append(pars)
        tits.append(secs)

    # create datasets
    pythonData = []
    modelData = []
    for t in tits:
        title = []
        for sec in t:
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
