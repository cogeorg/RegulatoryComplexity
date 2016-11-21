from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import math
import random
from features import *


# read data
f = open ("test_layer1.txt", "r")

# save words as tuples
words = []
for line in f:
    word = line.split("\t")
    wordTup = (word[0], word[1], word[2], word[3], word[4])
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
trainNo = int(math.floor(0.7 * sentNo))
print "Training size: ", trainNo
restNo = sentNo - trainNo
valNo = int(math.floor(0.6 * restNo))
print "Validation size: ", valNo
testNo = restNo - valNo
print "Test size: ", testNo

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

# cross Validation
cv = []

# define feature radius
radius = range(3, 5)

# hpyerparameters
c1 = [2**i for i in range(-10, -3)]
c2 = [2**i for i in range(-5, -3)]
maxIt = range(20, 55, 5)

for r in radius:

    # train and val sets in CRFsuite format
    xtrain = [sent2features(s, r) for s in train]
    ytrain = [sent2labels(s) for s in train]

    xval = [sent2features(s, r) for s in val]
    yval = [sent2labels(s) for s in val]

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
                print r, i, j, k, accuracy

cv.sort(key=lambda x: x[4])
print cv[0], cv[len(cv)-1]

# out of sample evaluation
r = cv[len(cv)-1][0]
c1 = cv[len(cv)-1][1]
c2 = cv[len(cv)-1][2]
maxIt = cv[len(cv)-1][3]

# train and test sets in CRFsuite format
xtrain = [sent2features(s, r) for s in train + val]
ytrain = [sent2labels(s) for s in train + val]

xtest = [sent2features(s, r) for s in test]
ytest = [sent2labels(s) for s in test]

trainer.set_params({
    'c1': c1,   # coefficient for L1 penalty
    'c2': c2,  # coefficient for L2 penalty
    'max_iterations': maxIt,

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
