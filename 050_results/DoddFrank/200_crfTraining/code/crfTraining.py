from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite


# read data
f = open ("title_1_par_1_layer1.txt", "r")

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
train = sentences[0:8]
val = sentences[8:10]
test = sentences[10:]

# define features
def word2features(sent, i):
    word = sent[i][0]
    posTag1 = sent[i][1]
    posTag2 = sent[i][2]
    depTag = sent[i][3]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'posTag1=' + posTag1,
        'posTag2=' + posTag2,
        'depTag' + depTag,
    ]
    if i > 0:
        word = sent[i-1][0]
        posTag1 = sent[i-1][1]
        posTag2 = sent[i-1][2]
        depTag = sent[i-1][3]
        features.extend([
            '-1:word.lower=' + word.lower(),
            '-1:word.istitle=%s' % word.istitle(),
            '-1:word.isupper=%s' % word.isupper(),
            '-1:word.isdigit=%s' % word.isdigit(),
            '-1:posTag1=' + posTag1,
            '-1:posTag2=' + posTag2,
            '-1:depTag=' + depTag,
        ])
    else:
        features.append('BOS')

    if i > 1:
        word = sent[i-2][0]
        posTag1 = sent[i-2][1]
        posTag2 = sent[i-2][2]
        depTag = sent[i-2][3]
        features.extend([
            '-2:word.lower=' + word.lower(),
            '-2:word.istitle=%s' % word.istitle(),
            '-2:word.isupper=%s' % word.isupper(),
            '-2:word.isdigit=%s' % word.isdigit(),
            '-2:posTag1=' + posTag1,
            '-2:posTag2=' + posTag2,
            '-2:depTag=' + depTag,
        ])

    if i < len(sent)-2:
        word = sent[i+2][0]
        posTag1 = sent[i+2][1]
        posTag2 = sent[i+2][2]
        depTag = sent[i+2][3]
        features.extend([
            '+2:word.lower=' + word.lower(),
            '+2:word.istitle=%s' % word.istitle(),
            '+2:word.isupper=%s' % word.isupper(),
            '+2:word.isdigit=%s' % word.isdigit(),
            '+2:posTag1=' + posTag1,
            '+2:posTag2=' + posTag2,
            '+2:depTag=' + depTag,
        ])
        
    if i < len(sent)-1:
        word = sent[i+1][0]
        posTag1 = sent[i+1][1]
        posTag2 = sent[i+1][2]
        depTag = sent[i+1][3]
        features.extend([
            '+1:word.lower=' + word.lower(),
            '+1:word.istitle=%s' % word.istitle(),
            '+1:word.isupper=%s' % word.isupper(),
            '+1:word.isdigit=%s' % word.isdigit(),
            '+1:posTag1=' + posTag1,
            '+1:posTag2=' + posTag2,
            '+1:depTag=' + depTag,
        ])
    else:
        features.append('EOS')
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, posTag1, posTag2, depTag, label in sent]

def sent2tokens(sent):
    return [token for token, posTag1, posTag2, depTag, label in sent]   


# train, val and test sets in CRFsuite format
xtrain = [sent2features(s) for s in train]
ytrain = [sent2labels(s) for s in train]


xval = [sent2features(s) for s in val]
yval = [sent2labels(s) for s in val]

xtest = [sent2features(s) for s in test]
ytest = [sent2labels(s) for s in test]

# train model
trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(xtrain, ytrain):
    trainer.append(xseq, yseq)

trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 50,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

trainer.train('title_1_par_1.crfsuite')

# make predictions
tagger = pycrfsuite.Tagger()
tagger.open('title_1_par_1.crfsuite')

example_sent = val[1]
print(' '.join(sent2tokens(example_sent)))

print("Predicted:", ' '.join(tagger.tag(sent2features(example_sent))))
print("Correct:  ", ' '.join(sent2labels(example_sent)))
