# Input:
# - python pickle file which contains a list(titles/books/.../aList) of lists(sections/chapters/categories/bList)of lists(sentences) of lists(words)
# - python pickle file which contains a list of lists(sentences) of lists(words)
# Output:
# - Word vectors
# - Sentence vectors
# - distances between consecutive sentences
# - graphs

################################################################################
import numpy as np
import os
import pickle
import gensim, logging
from gensim import corpora, models, similarities
import plotly
import plotly.graph_objs as go
import argparse
################################################################################

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

################################################################################

def main(argv):
    cwd = os.getcwd()
    # import model training data
    with open(cwd + argv.input + 'modelData','rb') as f:
         data = pickle.load(f)

    # import aList
    with open(cwd + argv.input + 'pythonData','rb') as g:
         aList = pickle.load(g)

    # word2vec training
    ####################
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
    epochs = 5             # number of epochs in NN

    # training
    model = gensim.models.Word2Vec(data, sg = skip_gram, size = features, window = context, min_count = count, workers = threads, negative = neg, iter = epochs)
    model.init_sims(replace=True)
    #model.save('outputModel')
    #model.save_word2vec_format('outputTxt')

    if argv.method == 'average':
        # create sentence vectors by averaging
        aListVec = []
        bListIndex = []
        for t in aList:
            sentVec = []
            index = []
            c = -1
            for bList in t:
                for s in bList:
                    c += 1
                    sVec = [0]*300
                    d = 0
                    for w in s:
                        try:
                            sVec += model[w]
                            d += 1
                        except:
                            continue
                    sVec = list(sVec)
                    try:
                        avSVec = [x/d for x in sVec]
                    except:
                        avSVec = sVec
                    sentVec.append(avSVec)
                    print len(sentVec)
                index.append(c)
            bListIndex.append(index[:-1])
            aListVec.append(sentVec)

    elif argv.method == 'tfidf':
        # create vectors by weighting with TF-IDF
        # TF-IDF
        d = 0
        dictionary = corpora.Dictionary(data)
        corpus = [dictionary.doc2bow(t) for t in data]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        # sentence vectors
        aListVec = []
        bListIndex = []
        for t in aList:
            sentVec = []
            index = []
            c = -1
            for bList in t:
                for s in bList:
                    c += 1
                    sVec = np.array([0]*300)
                    for f, w in enumerate(s):
                        try:
                            sVec = sVec + np.array([corpus_tfidf[d][f][1]*x for x in model[w]])
                        except:
                            continue
                    sVec = list(sVec)
                    sentVec.append(sVec)
                    print len(sentVec)
                    d += 1
                index.append(c)
            bListIndex.append(index[:-1])
            aListVec.append(sentVec)

    # calculate distances per aList
    aListDist = []
    for t in aListVec:
        dists = distances(t)
        aListDist.append(dists)

    # visualize
    c = int(argv.start)
    for j, t in enumerate(aListDist):

        # calculate mean and std derivation
        arr = np.array(t)
        m = np.mean(arr, axis=0)
        std = np.std(arr, axis=0)

        # vertical lines
        lines = []
        for i in bListIndex[j]:
            line = dict({'type': 'line', 'x0': i, 'y0': 0, 'x1': i, 'y1': 1, 'opacity': 0.2})
            lines.append(line)

        # plot
        trace0 = go.Scatter(y = t, mode = 'lines')
        data = go.Data([trace0])
        layout = go.Layout(title = argv.title + ' %s' %c, xaxis = {'title':'Sentences<br>Mean: %s, Standard Deviation: %s' %(m, std)}, yaxis = {'title':'Distances'}, shapes = lines)
        figure = go.Figure(data = data, layout = layout)
        plotly.offline.plot(figure, filename = cwd + argv.output + argv.title + '_%s_'%c + argv.method + '.html', auto_open = False)
        c += 1

################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Word Embeddings')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-m', '--method', help='Vector Aggregation Method', required=True)
    parser.add_argument('-t', '--title', help='Title', required=True)
    parser.add_argument('-s', '--start', help='Start', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
