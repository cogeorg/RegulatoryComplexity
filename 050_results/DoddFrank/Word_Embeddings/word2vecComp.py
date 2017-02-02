# Input:
# - python pickle files which contain a list(titles/books/.../aList) of lists(sections/chapters/categories/bList)of lists(sentences) of lists(words)
# - python pickle files which contain a list of lists(sentences) of lists(words)
# Output:
# - Word vectors
# - Sentence vectors
# - distances between consecutive sentences
# - graphs

################################################################################
import numpy as np
import os
import pickle
import math
import gensim, logging
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

    folders = argv.inputlist

    # allData = []
    # aListData = []
    # for item in folders:
    #     # import model training data
    #     with open(cwd + argv.input + item + '/' + 'modelData','rb') as f:
    #         data = pickle.load(f)
    #         allData += data
    #     # import sentences per document
    #     with open(cwd + argv.input + item + '/' + 'pythonData','rb') as g:
    #          aList = pickle.load(g)
    #          aListData.append(aList)

    dataList = []
    length = []
    aListData = []
    for item in folders:
        # import model training data
        with open(cwd + argv.input + item + '/' + 'modelData','rb') as f:
            data = pickle.load(f)
            dataList.append(data)
            length.append(len(data))
        # import sentences per document
        with open(cwd + argv.input + item + '/' + 'pythonData','rb') as g:
             aList = pickle.load(g)
             aListData.append(aList)

    allData = []
    maxim = max(length)
    for item in dataList:
        sFactor = int(math.floor(maxim/len(item)))
        allData += sFactor*item


    # word2vec training
    ####################
    # screen output
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # parameters
    skip_gram = 1           # use skip gram model
    features = 300          # Word vector dimensionality
    count = 3               # Minimum word count
    threads = 8             # Number of threads to run in parallel
    context = 5             # Context window size
    downsampling = 1e-3     # Downsample setting for frequent words
    neg = 5                 # negative sample
    epochs = 5             # number of epochs in NN

    # training
    model = gensim.models.Word2Vec(allData, sg = skip_gram, size = features, window = context, min_count = count, workers = threads, negative = neg, iter = epochs)
    model.init_sims(replace=True)
    #model.save('outputModel')
    #model.save_word2vec_format('outputTxt')

    # processing for both documents:
    means = []
    stds = []
    for k, l in enumerate(aListData):

        # create sentence vectors by averaging
        aListVec = []
        bListIndex = []
        for t in l:
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
                index.append(c)
            bListIndex.append(index[:-1])
            aListVec.append(sentVec)

        # calculate distances per aList
        aListDist = []
        for t in aListVec:
            dists = distances(t)
            aListDist.append(dists)

        # visualize
        c = 0
        titleMean = []
        titleStd = []
        for j, t in enumerate(aListDist):

            # calculate mean and std derivation
            arr = np.array(t)
            m = np.mean(arr, axis=0)
            std = np.std(arr, axis=0)
            titleMean.append(m)
            titleStd.append(std)

            # vertical lines
            lines = []
            for i in bListIndex[j]:
                line = dict({'type': 'line', 'x0': i, 'y0': 0, 'x1': i, 'y1': 1, 'opacity': 0.2})
                lines.append(line)

            # plot
            trace0 = go.Scatter(y = t, mode = 'lines')
            data = go.Data([trace0])
            layout = go.Layout(title = folders[k] + ' %s' %c, xaxis = {'title':'Sentences<br>Mean: %s, Standard Deviation: %s' %(m, std)}, yaxis = {'title':'Distances'}, shapes = lines)
            figure = go.Figure(data = data, layout = layout)
            plotly.offline.plot(figure, filename = cwd + argv.output + folders[k] + '_%s.html' %c, auto_open = False)
            c += 1

        means.append([folders[k], titleMean])
        stds.append([folders[k], titleStd])

    means = sorted(means)
    stds = sorted(stds)

    # # save means and stds
    # Means = np.zeros((j+1,k+1))
    # Stds = np.zeros((j+1,k+1))
    #
    # for a, m in enumerate(means):
    #     for b, n in enumerate(m[1]):
    #         Means[b,a] = n
    #
    # for a, m in enumerate(stds):
    #     for b, n in enumerate(m[1]):
    #         Stds[b,a] = n
    #
    # np.savetxt(cwd + argv.output + 'Means.txt', Means)
    # np.savetxt(cwd + argv.output + 'Stds.txt', Stds)
    #
    # # plot means and stds
    # traces = []
    # for i in range(len(titleMean)):
    #     trace = go.Scatter(y = Means[i,:], mode = 'lines', name='Title %s' %i)
    #     traces.append(trace)
    # data = go.Data(traces)
    # layout = go.Layout(title = 'Means per Version', xaxis = {'title':'Versions', 'tickvals': range(len(titleMean)), 'ticktext': sorted(folders)}, yaxis = {'title':'Mean'})
    # figure = go.Figure(data = data, layout = layout)
    # plotly.offline.plot(figure, filename = cwd + argv.output + 'Means.html', auto_open = False)
    #
    # traces = []
    # for i in range(len(titleMean)):
    #     trace = go.Scatter(y = Stds[i,:], mode = 'lines', name='Title %s' %i)
    #     traces.append(trace)
    # data = go.Data(traces)
    # layout = go.Layout(title = 'Standard Deviation per Version', xaxis = {'title':'Versions', 'tickvals': range(len(titleMean)), 'ticktext': sorted(folders)}, yaxis = {'title':'Standard Deviation'})
    # figure = go.Figure(data = data, layout = layout)
    # plotly.offline.plot(figure, filename = cwd + argv.output + 'Stds.html', auto_open = False)


################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Word Embeddings')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-l', '--inputlist', nargs='+', help='Input Folders', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
