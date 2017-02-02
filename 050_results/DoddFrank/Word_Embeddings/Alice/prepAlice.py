import os
import pickle
import argparse
import re
from nltk import sent_tokenize

# prepocessing
################################################################################
def main(argv):
    cwd = os.getcwd()

    # parse text
    with open(cwd + argv.input + 'carroll-alice.txt', 'r') as alice:

        book = []
        chapter = []
        text = ''
        for line in alice:
            if line.startswith('CHAPTER'):
                chapter.append(text)
                book.append(chapter)
                chapter = []
                text = ''
            elif not re.match(r'\s', line):
                line = line.replace('\n', ' ')
                text += line
            else:
                continue
    chapter.append(text)
    book.append(chapter)
    book = book[1:]

    # split into sentences and correct errors
    alice = []
    for c in book:
        chapter = []
        for string in c:
            sents = sent_tokenize(string)
            for s in sents:
                if s[0].islower():
                    chapter[-1] = chapter[-1] + ' ' + s
                else:
                    chapter.append(s)
        alice.append(chapter)

    # split into words, clean words
    pythonData = []
    modelData = []
    for c in alice:
        sentences = []
        for s in c:
            words = re.findall(r"[\w']+", s)
            cleanWords = []
            for w in words:
                w = w.strip("'")
                w = w.strip(',')
                w = w.strip(';')
                w = w.strip(':')
                w = w.strip('.')
                w = w.strip('!')
                w = w.strip('?')
                w = w.strip('"')
                w = w.lower()
                if w:
                    cleanWords.append(w)
            sentences.append(cleanWords)
            modelData.append(cleanWords)
        pythonData.append(sentences)

    pythonData = [pythonData]

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
