import os
import pickle
import argparse
import re

# split functions
###############################################################################

def split_before(pattern,text):
    prev = 0
    for m in re.finditer(pattern,text):
        yield text[prev:m.start()]
        prev = m.start()
    yield text[prev:]

def iter_split(ind, text):
    lineSplit = list(split_before(re.escape(ind[1]), text))
    nextInd = re.findall(r'[0-9]+:[0-9]+', lineSplit[1])
    if len(nextInd) > 1:
        return [lineSplit[0]] + iter_split(nextInd, lineSplit[1])
    else:
        return lineSplit


# prepocessing
################################################################################
def main(argv):
    cwd = os.getcwd()
    with open(cwd + argv.input + 'bible-kjv.txt', 'r') as bible:
        text = []
        book = []
        line = ''
        n = 0
        for item in bible:
            if item.startswith('1:1 '):
                book.append(line)
                text.append(book)
                line = item
                book = []
                n = 0
            else:
                if item == '\n':
                    n += 1
                else:
                    if n == 0:
                        line += item
                    elif n == 1:
                        book.append(line)
                        line = item
                        n = 0
                    else:
                        n = 0
        text.append(book)
        text = text[1:]

    # split into verses
    bible = []
    for b in text:
        book = []
        for s in b:
            s = ' '.join(s.split())
            ind = re.findall(r'[0-9]+:[0-9]+', s)
            if len(ind) > 1:
                book += iter_split(ind, s)
            else:
                book.append(s)
        bible.append(book)

    # split into chapters
    text = []
    for book in bible:
        chaps = []
        chapter = []
        c = 1
        for item in book:
            chap = re.findall(r'(^[0-9]{1,3}):', item)
            if chap == c:
                item = re.sub(r'[0-9].*?\s', '', item)
                chapter.append(item)
            else:
                if chapter:
                    chaps.append(chapter)
                chapter = []
                c = chap
                item = re.sub(r'[0-9].*?\s', '', item)
                chapter.append(item)
        if chapter:
            chaps.append(chapter)
        text.append(chaps)

    # save data
    pythonData = []
    modelData = []
    for book in text:
        chapters = []
        for c in book:
            sentences = []
            for s in c:
                words = s.split(' ')
                cleanWords = []
                for w in words:
                    w = w.strip(',')
                    w = w.strip(';')
                    w = w.strip(':')
                    w = w.strip('.')
                    w = w.strip('!')
                    w = w.strip('?')
                    w = w.strip('"')
                    w = w.lower()
                    cleanWords.append(w)
                sentences.append(cleanWords)
                modelData.append(cleanWords)
            chapters.append(sentences)
        pythonData.append(chapters)

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
