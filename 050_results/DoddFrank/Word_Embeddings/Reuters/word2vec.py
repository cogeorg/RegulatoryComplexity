from nltk.corpus import reuters
from nltk import tokenize
import gensim, logging
import numpy as np
import matplotlib.pyplot as plt

files = reuters.fileids()

# articles with category earn and length > 1000
earn = []
for f in files:
    if 'earn' in reuters.categories(f):
        if len(reuters.raw(f)) > 1000:
            earn.append(f)
# 388 articles

articles = []
allData = []
for a in earn:
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
        allData.append(words)
    articles.append(sentences)


# word2vec training
############################################################################
# screen output
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# parameters
skip_gram = 1           # use skip gram model
features = 300          # Word vector dimensionality
count = 3               # Minimum word count
threads = 4             # Number of threads to run in parallel
context = 5             # Context window size
downsampling = 1e-3     # Downsample setting for frequent words
neg = 5                 # negative sample
epochs = 10             # number of epochs in NN

model = gensim.models.Word2Vec(allData, sg = skip_gram, size = features, window = context, min_count = count, workers = threads, negative = neg, iter = epochs)
model.init_sims(replace=True)
model.save('outputModel')
model.save_word2vec_format('outputTxt')


# distance function
def distances(vector):
    dists = []
    for i in range(len(vector)):
        if i > 0:
            x = np.array(vector[i])
            y = np.array(vector[i-1])
            d = np.linalg.norm(x - y)
            dists.append(d)
    return dists

# create sentence vectors
c = 0
artIndex = []
sentVec = []
for a in articles:
    c += 1
    index = []
    for s in a:
        sVec = [0]*300
        d = 0
        for w in s:
            try:
                sVec += model[w]
                d += 1
            except:
                continue
        index.append(c)
        sVec = list(sVec)
        try:
            avSVec = [x/d for x in sVec]
        except:
            avSVec = sVec
        sentVec.append(avSVec)
    artIndex += index

# calculate distances
dists = distances(sentVec)

# calculate indices for plotting
inds = []
c = -1
for i in range(0, len(artIndex)):
    if artIndex[i] > artIndex[i-1]:
        inds.append(c)
    c += 1

for i in inds:
    plt.axvline(x = i, color = 'r')
plt.title('Earn')
plt.plot(dists)
#plt.savefig('earn.png', dpi=1200)
#plt.clf()
plt.show()
