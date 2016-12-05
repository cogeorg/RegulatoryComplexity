from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import math
import random
import numpy
from features import *
from config import *
import argparse

# cross validation function
def cv(layer, radius, c1, c2, maxIt, cvRounds, train, val, step):
    try:
        rounds = range(len(cvRounds))
    except:
        rounds = [0]
    for d in rounds:
        cv = []

        for r in radius:

            # train and val sets in CRFsuite format
            xtrain = [sent2features(s, r, layer) for s in train]
            ytrain = [sent2labels(s, layer) for s in train]

            xval = [sent2features(s, r, layer) for s in val]
            yval = [sent2labels(s, layer) for s in val]

            # train model
            trainer = pycrfsuite.Trainer(verbose=False)

            for xseq, yseq in zip(xtrain, ytrain):
                trainer.append(xseq, yseq)

            for i in c1:
                for j in c2:
                    for k in maxIt:

                        trainer.set_params({
                            'c1': i,   # coefficient for L1 penalty
                            'c2': j,  # coefficient for L2 penalty
                            'max_iterations': k,

                            # include transitions that are possible, but not observed
                            'feature.possible_transitions': True
                        })

                        trainer.train('test.crfsuite')

                        # make predictions
                        tagger = pycrfsuite.Tagger()
                        tagger.open('test.crfsuite')

                        # evaluate model
                        ypred = [tagger.tag(xseq) for xseq in xval]
                        error = 0
                        n = 0
                        for l in range(len(ypred)):
                            for m in range(len(ypred[l])):
                                if yval[l][m] != ypred[l][m]:
                                    error += 1
                                n += 1
                        accuracy = 1 - float(error)/n
                        #print "Accuracy: ", accuracy

                        cv.append([r, i, j, k, accuracy])
                        #print r, i, j, k, accuracy

        cv.sort(key=lambda x: x[4])
        print cv[-1]

        # refinement
        r = range(min(cv[-1][0], cv[-2][0]), max(cv[-1][0], cv[-2][0])+1)
        c1 = list(numpy.arange(min(cv[len(cv)-1][1], cv[len(cv)-2][1]), max(cv[len(cv)-1][1], cv[len(cv)-2][1]), 0.01**(d+2)))
        c2 = list(numpy.arange(min(cv[len(cv)-1][2], cv[len(cv)-2][2]), max(cv[len(cv)-1][2], cv[len(cv)-2][2]), 0.01**(d+2)))
        if step-2 > 0:
            step = step-2
            maxIt = range(min(cv[-1][3], cv[-2][3]), max(cv[-1][3], cv[-2][3])+1, step)


    r = cv[-1][0]
    c1 = cv[-1][1]
    c2 = cv[-1][2]
    maxIt = cv[-1][3]
    return [r, c1, c2, maxIt]

def main(argv):

    for layer in [1,2,3]:
        print 'Layer', layer

        f = open (argv.input + "data_layer_" + str(layer) + ".txt", "r")

        # save words as tuples
        words = []
        for line in f:
            line = line.strip()
            word = line.split("\t")
            wordTup = tuple(word)
            words.append(wordTup)

        # save sentences as lists
        sentences = []
        sentence = []
        for word in words:
            if word[0] == word[1] == word[2] == ".":
                sentence.append(word)
                sentences.append(sentence)
                sentence = []
            else:
                sentence.append(word)

        # split in train, val and test sets
        sentNo = len(sentences)
        trainNo = int(math.floor(0.8 * sentNo))
        #print "Training size: ", trainNo
        restNo = sentNo - trainNo
        valNo = int(math.floor(0.7 * restNo))
        #print "Validation size: ", valNo
        testNo = restNo - valNo
        #print "Test size: ", testNo

        # shuffle sentences
        random.seed(2016)
        x = range(sentNo)
        random.shuffle(x)
        sentShuffle = []
        for i in range(len(x)):
            sentShuffle.append(sentences[x[i]])

        # define train, validation and test set
        train = sentShuffle[0:trainNo]
        val = sentShuffle[trainNo:trainNo + valNo]
        test = sentShuffle[trainNo + valNo:]

        # cross validation
        output = cv(layer, radius, c1, c2, maxIt, cvRounds, train, val, step)
        rOpt = output[0]
        c1Opt = output[1]
        c2Opt = output[2]
        maxItOpt = output[3]

        with open(argv.output + "settings.txt", "a") as g:
            g.write(str(layer) + '\t' + str(rOpt) + '\t' + str(c1Opt) + '\t' + str(c2Opt) + '\t'+ str(maxItOpt))

        # out of sample evaluation
        #r = cv[len(cv)-1][0]
        #c1 = cv[len(cv)-1][1]
        #c2 = cv[len(cv)-1][2]
        #maxIt = cv[len(cv)-1][3]

        # train and test sets in CRFsuite format
        xtrain = [sent2features(s, rOpt, layer) for s in train + val]
        ytrain = [sent2labels(s, layer) for s in train + val]

        xtest = [sent2features(s, rOpt, layer) for s in test]
        ytest = [sent2labels(s, layer) for s in test]

        # train model
        trainer = pycrfsuite.Trainer(verbose=False)

        for xseq, yseq in zip(xtrain, ytrain):
            trainer.append(xseq, yseq)

        trainer.set_params({
            'c1': c1Opt,   # coefficient for L1 penalty
            'c2': c2Opt,  # coefficient for L2 penalty
            'max_iterations': maxItOpt,

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })

        trainer.train('test.crfsuite')

        # make predictions
        tagger = pycrfsuite.Tagger()
        tagger.open('test.crfsuite')

        # evaluate model
        ypred = [tagger.tag(xseq) for xseq in xtest]
        error = 0
        n = 0
        for i in range(len(ypred)):
            for j in range(len(ypred[i])):
                if ytest[i][j] != ypred[i][j]:
                    error += 1
                n += 1
        accuracy = 1 - float(error)/n
        print "Accuracy: ", accuracy

'''
for item in val:
    example_sent = item
    print(' '.join(sent2tokens(example_sent)))

    print("Predicted:", ' '.join(tagger.tag(sent2features(example_sent))))
    print("Correct:  ", ' '.join(sent2labels(example_sent)))

'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CRF Training.')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
