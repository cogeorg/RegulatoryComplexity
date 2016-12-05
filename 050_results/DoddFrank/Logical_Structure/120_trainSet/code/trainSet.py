import os
import glob
import argparse

def main(argv):
    # load pos
    pos = []
    for f in os.listdir(argv.pos):
        if f.endswith(".txt"):
            with open(argv.pos + "/" + f, "r") as f:
                for line in f:
                    word = line.split("\t")
                    pos.append(word[:-1])

    # load parse
    parse = []
    for f in os.listdir(argv.parser):
        if f.endswith(".txt"):
            with open(argv.parser + "/" + f, "r") as f:
                for line in f:
                    word = line.split("\t")
                    parse.append(word[:-1])



    # train set for each layer
    if len(pos) == len(parse):
        l = len(pos)
        trainLayers = []
        for j in range(2, 5):
            trainLayer = []
            i = 0
            while i < l:
                if pos[i][0] == ".":
                    trainLayer.append(pos[i] + (j-1) * ["O"])
                else:
                    trainLayer.append(pos[i] + parse[i][1:j])
                i += 1
            trainLayers.append(trainLayer)
    else:
        print "Sets don't match."

    # save output
    n = 1
    for layer in trainLayers:
        f = open(argv.output + 'data_layer_%s.txt' %n,'w')
        for word in layer:
            for item in word:
                f.write("%s\t" %item)
            f.write("\n")
        f.close()
        n += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates Data Set for CRF.')
    parser.add_argument('-p', '--pos', help='Input POS Directory', required=True)
    parser.add_argument('-q', '--parser', help='Input Parser Directory', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
