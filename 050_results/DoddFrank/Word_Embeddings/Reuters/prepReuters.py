from nltk.corpus import reuters
from nltk import tokenize
import os
import pickle
import argparse


def main(argv):
    cwd = os.getcwd()

    files = reuters.fileids()
    categories = ['acq', 'earn', 'gnp', 'gold', 'income', 'interest', 'money-fx', 'money-supply', 'retail', 'trade']

    # filter out articles for each category with more than 1000 characters
    news = []
    for c in categories:
        articles = []
        for f in files:
            if c in reuters.categories(f):
                if len(reuters.raw(f)) > 1000:
                    articles.append(f)
        news.append(articles)


    pythonData = []
    modelData = []
    for c in news:
        articles = []
        for a in c:
            rawText = reuters.raw(a)
            rawText = rawText.strip()
            # remove headlines
            rawText = rawText.split('\n', 1)[-1]
            # remove extra spaces
            rawText = ' '.join(rawText.split())
            # delete html tags
            rawText = rawText.replace('&lt;', '')
            rawText = rawText.replace('>', '')
            # split into sentences
            sents = tokenize.sent_tokenize(rawText)
            # split into words
            sentences = []
            for s in sents:
                words = s.split(' ')
                cleanWords = []
                for c, w in enumerate(words, start=1):
                    w = w.strip(',')
                    w = w.strip(';')
                    w = w.strip(':')
                    if c == len(words):
                        w = w.strip('.')
                    w = w.strip('"')
                    w = w.lower()
                    cleanWords.append(w)
                sentences.append(cleanWords)
                modelData.append(cleanWords)
            articles.append(sentences)
        pythonData.append(articles)

    # save datasets
    with open(cwd + argv.output + 'pythonData', 'w') as f:
        pickle.dump(pythonData, f)
    with open(cwd + argv.output + 'modelData', 'w') as g:
        pickle.dump(modelData, g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank')
    parser.add_argument('-i', '--input', help='Input Directory', required=False)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
