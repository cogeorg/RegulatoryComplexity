# Function that extracts features given a certain radius

def word2features(sent, i, r):

    r += 1
    radius = range(1,r)

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
        'depTag=' + depTag,
    ]

    for r in radius:
        if i == 0:
            features.append('BOS')
        if i >= r:
            word = sent[i-r][0]
            posTag1 = sent[i-r][1]
            posTag2 = sent[i-r][2]
            depTag = sent[i-r][3]
            features.extend([
                '-' + str(r) + ':word.lower=' + word.lower(),
                '-' + str(r) + ':word.istitle=%s' % word.istitle(),
                '-' + str(r) + ':word.isupper=%s' % word.isupper(),
                '-' + str(r) + ':word.isdigit=%s' % word.isdigit(),
                '-' + str(r) + ':posTag1=' + posTag1,
                '-' + str(r) + ':posTag2=' + posTag2,
                '-' + str(r) + ':depTag=' + depTag,
            ])
        if i < len(sent)-r:
            word = sent[i+r][0]
            posTag1 = sent[i+r][1]
            posTag2 = sent[i+r][2]
            depTag = sent[i+r][3]
            features.extend([
                '+' + str(r) + ':word.lower=' + word.lower(),
                '+' + str(r) + ':word.istitle=%s' % word.istitle(),
                '+' + str(r) + ':word.isupper=%s' % word.isupper(),
                '+' + str(r) + ':word.isdigit=%s' % word.isdigit(),
                '+' + str(r) + ':posTag1=' + posTag1,
                '+' + str(r) + ':posTag2=' + posTag2,
                '+' + str(r) + ':depTag=' + depTag,
            ])
        if i == len(sent):
            features.append('EOS')

    return features

def sent2features(sent, r):
    return [word2features(sent, i, r) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, posTag1, posTag2, depTag, label in sent]

def sent2tokens(sent):
    return [token for token, posTag1, posTag2, depTag, label in sent]
