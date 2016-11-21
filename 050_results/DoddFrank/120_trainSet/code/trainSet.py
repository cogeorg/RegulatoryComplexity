import os
import glob

# load pos
pos = []
for item in glob.glob("*pos.txt"):
    with open(item, "r") as f:
        for line in f:
            word = line.split("\t")
            pos.append(word[:-1])

# load parse
parse = []
for item in glob.glob("*parse.txt"):
    with open(item, "r") as f:
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
                trainLayer.append(pos[i] + i * ["O"])
            else:
                trainLayer.append(pos[i] + parse[i][1:j])
            i += 1
        trainLayers.append(trainLayer)
else:
    print "Sets don't match."

os.chdir('/home/sabine/Dokumente/Git/RegulatoryComplexity/050_results/DoddFrank/120_trainSet/output')

# save output
n = 1
for layer in trainLayers:
    f = open('test_layer%s.txt' %n,'w')
    for word in layer:
        for item in word:
            f.write("%s\t" %item)
        f.write("\n")
    f.close()
    n += 1
