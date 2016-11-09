import re
import glob
from bs4 import BeautifulSoup
import os

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


for f in glob.glob("*.html"):

    # save name
    fileName = re.findall("(.*?)\.", f)[0]

    # open files in designated folder
    with open (f, "r") as myfile:
        data = myfile.read()

    # find all paragraphs
    paragraphs = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)

    #loop through paragraphs
    final = []
    for par in paragraphs:

        # Beautiful Soup to parse it and to find all spans
        soup = BeautifulSoup(par)
        spans = soup.find_all('span')

        # define a list with text in first entry and tags as list in second entry
        spanList=[]
        for span in spans:
            part = span.get_text()
            part = part.encode("utf-8")
            part = re.sub(r"`", "", part)
            part = re.sub(r"'", "", part)
            span = str(span)
            span = re.sub(":", ".", span)
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

        '''


        while i < len(spanList):
            # non-complex spans are saved right away
            if len(spanList[i][1]) == 1:
                output.append([spanList[i][0], spanList[i][1] + [None, None]])
                i += 1
            # semi-complex spans (2 layers) are split by second layer and parts are saved
            elif len(spanList[i][1]) == 2:
                # 2-layer span and type
                complSpan = spanList[i][0]
                complSpanType = spanList[i][1][0]
                # splitting part and type = 2nd layer
                splitSpan = spanList[i+1][0]
                splitSpanType = spanList[i+1][1][0]
                # split
                split = complSpan.split(splitSpan)
                #append output with first entry of split, splitting part, second entry of split
                output.append([split[0].strip(), [complSpanType, None, None]])
                output.append([splitSpan, [complSpanType, splitSpanType, None]])
                output.append([split[1].strip(), [complSpanType, None, None]])
                i += 2
            # complex spans (various layers)
            else:
                # most complex span and type
                complSpan = spanList[i][0]
                complSpanType = spanList[i][1][0]
                # complexity
                compl = len(spanList[i][1])
                # less complex spans
                spans = spanList[i+1:i+compl]
                # process non- and semi-complex spans as above
                otherSpans = []
                k = 0
                while k < len(spans):
                    if len(spans[k][1]) == 1:
                        otherSpans.append([spans[k][0], [complSpanType, spans[k][1][0], None]])
                        k += 1
                    else:
                        upSpan = spans[k][0]
                        upSpanType = spans[k][1][0]
                        splitSpan = spans[k+1][0]
                        splitSpanType = spans[k+1][1][0]
                        split = upSpan.split(splitSpan)
                        if split[0]: otherSpans.append([split[0].strip(), [complSpanType, upSpanType, None]])
                        otherSpans.append([splitSpan, [complSpanType, upSpanType, splitSpanType]])
                        if split[1]: otherSpans.append([split[1].strip(), [complSpanType, upSpanType, None]])
                        k += 2
                # loop through preprocessed spans
                for j in range(len(otherSpans)):
                    #current span
                    span = otherSpans[j][0]
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
                        output.append([split.strip(), [complSpanType, None, None]])
                        # than append current span
                        output.append(otherSpans[j])
                        # remove both from complex span
                        complSpan = complSpan[len(split):].strip()
                        complSpan = complSpan[len(span):].strip()
                # if something remains, append it in the end
                if splitt[1]:
                    output.append([splitt[1].strip(), [complSpanType, None, None]])
                i = i + compl
    '''

        # remove headlines and split in words
        abbrev = [r"(U\.S\.C\.)", r"(U\.S\.)", r"(seq\.)", r"(App\.)", r"(\.'')"]
        repl = ["U_S_C_", "U_S_", "seq_", "App_", "_''"]
        words = []
        for item in output:
            if item[1][0] == 'H': continue
            else:
                line = item[0]
                for a in abbrev:
                    line = re.sub(a, repl[abbrev.index(a)], line)
                word = line.split()
                for w in word:
                    words.append([w, item[1]])

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

        # resubstitute "_", replace ":", "(" and ")"
        for word in listIn:
            w = word[0]
            w = re.sub("_", ".", w)
            w = re.sub(":", ".", w)
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
                listIOB.append([listOut[i][0], 'O', 'O', 'O'])
            else:
                listIOB.append([listOut[i][0], layersIOB[0][i], layersIOB[1][i], layersIOB[2][i]])
            i += 1
        final.append(listIOB)


    os.chdir('/home/sabine/Dokumente/Git/RegulatoryComplexity/050_results/DoddFrank/100_parsedOutputs/output')

    # save output
    g = open(fileName + '.txt','w')
    for par in final:
        for word in par:
            for item in word:
                g.write("%s\t" %item)
            g.write("\n")
    g.close()

    # change back to right directory
    os.chdir('/home/sabine/Dokumente/Git/RegulatoryComplexity/050_results/DoddFrank/100_parsedOutputs/code')
