import re
import glob
from bs4 import BeautifulSoup
import os
import argparse

# function to untangle spans
def untangle(spanList, i, output, complSpans):
    n = 0
    while i < len(spanList):
        #if i != n:
        #     if complSpans: complSpans.pop(len(complSpans)-1)
        #print i, n, spanList[i], complSpans
        if len(spanList[i][1]) == 1:
            output.append([spanList[i][0], complSpans + spanList[i][1]])
            i += 1
        # semi-complex spans (2 layers) are split by second layer and parts are saved
        elif len(spanList[i][1]) == 2:
            # 2-layer span and type
            complSpan = spanList[i][0]
            complSpanType = spanList[i][1][0]
            complSpans = complSpans + [complSpanType]
            # splitting part and type = 2nd layer
            splitSpan = spanList[i+1][0]
            splitSpanType = spanList[i+1][1][0]
            # split
            split = complSpan.split(splitSpan)
            #append output with first entry of split, splitting part, second entry of split
            if split[0]:
                output.append([split[0].strip(), complSpans])
            output.append([splitSpan, complSpans + [splitSpanType]])
            if split[1]:output.append([split[1].strip(), complSpans])
            complSpans = complSpans[:-1]
            i += 2
        # complex spans (various layers)
        else:
            # most complex span and type
            complSpan = spanList[i][0]
            complSpanType = spanList[i][1][0]
            complSpans = complSpans + [complSpanType]
            # complexity
            compl = len(spanList[i][1])
            # less complex spans
            spans = spanList[i+1:i+compl]
            # process non- and semi-complex spans as above
            otherSpans = []
            k = 0
            # call itself
            untangle(spans, k, otherSpans, complSpans)
            # loop through preprocessed spans
            for j in range(len(otherSpans)):
                #current span
                span = otherSpans[j][0].strip()
                # split with current span as separator
                splitt = complSpan.split(span)
                # only consider first entry in split-list
                split = splitt[0]
                # if first entry is empty, save current span and remove it from complex span
                if not split:
                    output.append(otherSpans[j])
                    complSpan = complSpan[len(span):].strip()
                # if first entry is non-empty
                else:
                    # append first first entry
                    output.append([split.strip(), otherSpans[j][1][:-1]])
                    # than append current span
                    output.append(otherSpans[j])
                    # remove both from complex span
                    complSpan = complSpan[len(split):].strip()
                    complSpan = complSpan[len(span):].strip()
            # if something remains, append it in the end
            if splitt[1]:
                output.append([splitt[1].strip(), otherSpans[j][1][:-1]])
            complSpans = complSpans[:-1]
            i = i + compl
        n=n+1
    return(output, complSpans)

def main(argv):
    for f in os.listdir(argv.input):
        if f.endswith(".html"):

            # save name
            fileName = re.findall("(.*?)\.", f)[0]

            # open files in designated folder
            with open (argv.input + "/" + f, "r") as myfile:
                data = myfile.read()

            # find all paragraphs
            paragraphs = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)

            #loop through paragraphs
            final = []
            for par in paragraphs:

                # Beautiful Soup to parse it and to find all spans
                soup = BeautifulSoup(par, "lxml")
                spans = soup.find_all('span')

                # define a list with text in first entry and tags as list in second entry
                spanList=[]
                for span in spans:
                    part = span.get_text()
                    part = part.encode("utf-8")
                    # delete quotes
                    part = re.sub(r"`", "", part)
                    part = re.sub(r"'", "", part)
                    # change number format
                    part = re.sub(r"(\$)([0-9]+),([0-9]+)", r"USD\2\3", part)
                    for i in range(3):
                        part = re.sub(r"(USD[0-9]+),([0-9]+)", r"\1\2", part)
                    span = str(span)
                    partType = re.findall("class=\"(.+?)\"", span)
                    spanList.append([part, partType])

                #for span in spanList:
                    #print span

                # untangle complex spans
                output = []
                i = 0
                untangle(spanList, i, output, [])

                for item in output:
                    l = len(item[1])
                    if l == 3:
                        continue
                    elif l == 2:
                        item[1] = item[1] + [None]
                    else:
                        item[1] = item[1] + [None, None]

                #for item in output:
                #    print item

                # remove headlines and split in words
                abbrev = [r"(U\.S\.C\.)", r"(U\.S\.)", r"(seq\.)", r"(App\.)", r"C\.F\.R\.", r"\.''\.\(", r"(\.'')"]
                repl = ["U_S_C_", "U_S_", "seq_", "App_", "C_F_R_", r"_''_\()", "_''"]
                words = []
                for item in output:
                    if item[1][0] == 'H': continue
                    else:
                        line = item[0]
                        for a in abbrev:
                            line = re.sub(a, repl[abbrev.index(a)], line)
                        # replace numbers /w dots
                        line = re.sub(r"([0-9])\.([0-9])", r"\1_\2", line)
                        word = line.split()
                        for w in word:
                            words.append([w, item[1]])
                #for w in words:
                #    print w

                # split off special characters
                specialChar = [".", ",", "(", ")",":",";"]
                specialCharRe = ["\.", ",", "\(", "\)",":",";"]
                listIn = words
                listOut = []
                for char in specialChar:
                    for word in listIn:
                        if re.search(specialCharRe[specialChar.index(char)], word[0]):
                                w = word[0].split(char)
                                for l in w[:-1]:
                                    if l: listOut.append([l, word[1]])
                                    listOut.append([char, word[1]])
                                if w[-1]: listOut.append([w[-1], word[1]])
                        else:
                            listOut.append(word)
                    listIn = listOut
                    listOut = []

                # resubstitute "_", "(" and ")"
                for word in listIn:
                    w = word[0]
                    w = re.sub("_", ".", w)
                    w = re.sub("\(", "-LRB-", w)
                    w = re.sub("\)", "-RRB-", w)
                    listOut.append([w, word[1][0], word[1][1], word[1][2]])

                # convert tags to IOB structure
                firLayer = []
                secLayer = []
                thiLayer = []
                for item in listOut:
                    firLayer.append(str(item[1]))
                    secLayer.append(str(item[2]))
                    thiLayer.append(str(item[3]))
                layers = [firLayer, secLayer, thiLayer]

                layersIOB = []
                for layer in layers:
                    l = len(layer)
                    if layer[0] != "None":
                        layerIOB = ["B-" + layer[0]]
                    else:
                        layerIOB = ["O"]
                    i = 1
                    while i < l:
                        if layer[i] == layer[i-1]:
                            tag = "I-" + layer[i]
                            tag = re.sub(".-None", "O", tag)
                            layerIOB.append(tag)
                        else:
                            tag = "B-" + layer[i]
                            tag = re.sub(".-None", "O", tag)
                            layerIOB.append(tag)
                        i += 1
                    layersIOB.append(layerIOB)

                l = len(listOut)
                i = 0
                listIOB = []
                while i < l:
                    if listOut[i][0] == ".":
                        if listOut[i-1][0] != ".":
                            listIOB.append([listOut[i][0], 'O', 'O', 'O'])
                    else:
                        listIOB.append([listOut[i][0], layersIOB[0][i], layersIOB[1][i], layersIOB[2][i]])
                    i += 1
                final.append(listIOB)


            # save output
            g = open(argv.output + fileName + '.txt','w')
            for par in final:
                for word in par:
                    for item in word:
                        g.write("%s\t" %item)
                    g.write("\n")
            g.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input Directory', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
