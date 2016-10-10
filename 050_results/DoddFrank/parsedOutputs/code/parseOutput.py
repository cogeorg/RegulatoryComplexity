import re
import glob
from bs4 import BeautifulSoup


for f in glob.glob("*.html"):

    # open files in designated folder
    with open (f, "r") as myfile:
        data = myfile.read()
    
    # find all paragraphs
    paragraphs = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)

    # Beautiful Soup to parse it and to find all spans
    soup = BeautifulSoup(paragraphs[0])
    spans = soup.find_all('span')

    # define a list with text in first entry and tags as list in second entry
    spanList=[]
    for span in spans:
        part = span.get_text()
        part = part.encode("utf-8")
        span = str(span)
        partType = re.findall("class=\"(.+?)\"", span)
        spanList.append([part, partType])

    # untangle complex spans
    output = []
    i = 0
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


    for thing in output:
        print thing


