import re
import os
import pickle
import argparse


# prepocessing
################################################################################
def main(argv):
    cwd = os.getcwd()

    with open(cwd + argv.input + 'KWGengl.txt') as f:

        titles = []
        title = []
        section = []
        flag = 0
        paragraph = ''
        for line in f:
            if flag == 0:
                if line.startswith('XI'):
                    flag = 1
                else:
                    continue
            elif flag == 1:
                if line.startswith('Division'):
                    section.append(paragraph)
                    title.append(section)
                    titles.append(title)
                    section = []
                    title = []
                    paragraph = ''
                elif (line.startswith('Section')) and len(line) < 15:
                    section.append(paragraph)
                    title.append(section)
                    section = []
                    paragraph = ''
                elif re.search(r'^\([0-9]+[a-z]*\)\s[A-Z0-9\(\)]', line):
                    section.append(paragraph)
                    paragraph = line + ' '
                elif re.search(r'^[0-9]{1,3}[a-z]*\s', line):
                    continue
                elif line.startswith('\x0c'):
                    continue
                elif line.startswith('\n'):
                    continue
                elif line.startswith('Part IV'):
                    section.append(paragraph)
                    title.append(section)
                    titles.append(title)
                    section = []
                    title = []
                    paragraph = ''
                    flag = 2
                else:
                    paragraph += line + ' '
            else:
                if line.startswith('Part'):
                    section.append(paragraph)
                    title.append(section)
                    titles.append(title)
                    section = []
                    title = []
                    paragraph = ''
                elif (line.startswith('Section')) and len(line) < 15:
                    section.append(paragraph)
                    title.append(section)
                    section = []
                    paragraph = ''
                elif re.search(r'^\([0-9]+[a-z]*\)\s[A-Z0-9\(\)]', line):
                    section.append(paragraph)
                    paragraph = line + ' '
                elif re.search(r'^[0-9]{1,3}[a-z]*\s', line):
                    continue
                elif line.startswith('\x0c'):
                    continue
                elif line.startswith('\n'):
                    continue
                else:
                    paragraph += line + ' '
    section.append(paragraph)
    title.append(section)
    titles.append(title)

    titles = titles[1:]

    tits = []
    title = []
    for t in titles:
        for sec in t:
            if len(sec) > 1:
                sec = sec[1:]
                title.append(sec)
            else:
                p = sec[0]
                p = re.sub(r'(^[A-Z][\s\S]*?\n\s)([A-EG-Z]|For|Findings)', r'\2', p)
                if re.search(r'\(Repealed\)', p):
                    p = ''
                if p.isupper():
                    p = ''
                p = p.strip()
                if p:
                    sec = [p]
                    title.append(sec)
        tits.append(title)
        title = []


    titles = []
    for t in tits:
        title = []
        for s in t:
            section = []
            for p in s:
                p = ' '.join(p.split())
                p = re.sub(r'^\([0-9]{1,3}[a-z]*\)', '', p)
                p = p.strip()
                if p.startswith('(Repealed)'):
                    p = ''
                p = re.sub(r'([0-9])\.([0-9])', r'\1_\2', p)
                p = p.strip()
                sents = p.split('.')

                paragraph = []
                for sent in sents:
                    if sent:
                        sent = sent.strip()
                        sent = re.sub(r'^[0-9]{1,2}', '', sent)
                        words = sent.split(' ')

                        cleanWords = []
                        for w in words:
                            w = w.strip()
                            w = w.strip(',')
                            w = w.strip(':')
                            w = w.strip(';')
                            w = w.strip('(')
                            w = w.strip(')')
                            w = w.strip('[')
                            w = w.strip(']')
                            w = w.lower()
                            if w:
                                cleanWords.append(w)
                        paragraph.append(cleanWords)
                section.append(paragraph)
            title.append(section)
        titles.append(title)

    # create datasets
    pythonData = []
    modelData = []
    for t in titles:
        if t:
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
