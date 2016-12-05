# Function that extracts features given a certain radius

def word2features(sent, i, r, layer):

    r += 1
    radius = range(1,r)

    # the word itself
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

    # higher order layers
    if layer == 2:
        layer1 = sent[i][4]
        features.extend([
            'layer1=' + layer1,
        ])
    elif layer == 3:
        layer1 = sent[i][4]
        layer2 = sent[i][5]
        features.extend([
            'layer1=' + layer1,
            'layer2=' + layer2,
        ])

    # the words left and right of the word of interest
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
            # higher order layers
            if layer == 2:
                layer1 = sent[i-r][4]
                features.extend([
                    '-' + str(r) + ':layer1=' + layer1,
                ])
            elif layer == 3:
                layer1 = sent[i-r][4]
                layer2 = sent[i-r][5]
                features.extend([
                    '-' + str(r) + ':layer1=' + layer1,
                    '-' + str(r) + ':layer2=' + layer2,
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
            # higher order layers
            if layer == 2:
                layer1 = sent[i+r][4]
                features.extend([
                    '+' + str(r) + ':layer1=' + layer1,
                ])
            elif layer == 3:
                layer1 = sent[i+r][4]
                layer2 = sent[i+r][5]
                features.extend([
                    '+' + str(r) + ':layer1=' + layer1,
                    '+' + str(r) + ':layer2=' + layer2,
                ])

        if i == len(sent):
            features.append('EOS')

    return features

def sent2features(sent, r, layer):
    return [word2features(sent, i, r, layer) for i in range(len(sent))]

def sent2labels(sent, layer):
    if layer == 1:
        return [label for token, posTag1, posTag2, depTag, label in sent]
    elif layer == 2:
        return [label for token, posTag1, posTag2, depTag, layer1, label in sent]
    else:
        return [label for token, posTag1, posTag2, depTag, layer1, layer2, label in sent]

def sent2tokens(sent):
    if layer == 1:
        return [token for token, posTag1, posTag2, depTag, label in sent]
    elif layer == 2:
        return [token for token, posTag1, posTag2, depTag, layer1, label in sent]
    else:
        return [token for token, posTag1, posTag2, depTag, layer1, layer2, label in sent]
