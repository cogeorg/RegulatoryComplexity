import re
import glob
from bs4 import BeautifulSoup


for f in glob.glob("*.html"):

    with open (f, "r") as myfile:
        data = myfile.read()
    
    paragraphs = re.findall("(<div\sclass=\"ex5\">.*?</div>)", data)
    
    soup = BeautifulSoup(paragraphs[0])
    spans = soup.find_all('span')

    spanList=[]
    for span in spans:
        part = span.get_text()
        part = part.encode("utf-8")
        span = str(span)
        partType = re.findall("class=\"(.+?)\"", span)
        spanList.append([part, partType])

    #for span in spanList:
        #print span

 
    output = []
    i = 0
    while i < len(spanList)-1:
        if len(spanList[i][1]) == 1:
            output.append([spanList[i][0], spanList[i][1] + [None, None]])
            i += 1

        if len(spanList[i][1]) == 2:
            complSpan = spanList[i][0]
            complSpanType = spanList[i][1][0]

            splitSpan = spanList[i+1][0]
            splitSpanType = spanList[i+1][1][0]

            split = complSpan.split(splitSpan)

            output.append([split[0].strip(), [complSpanType, None, None]])
            output.append([splitSpan, [complSpanType, splitSpanType, None]])
            output.append([split[1].strip(), [complSpanType, None, None]])

            i += 2

        if len(spanList[i][1]) > 2:
            complSpan = spanList[i][0]
            complSpanType = spanList[i][1][0]

            compl = len(spanList[i][1])
            spans = spanList[i+1:i+compl]

            otherSpans = []
            k = 0
            while k < len(spans)-1:
                if len(spans[k][1]) == 1:
                    otherSpans.append([spans[k][0], [complSpanType, spans[k][1][0], None]])
                    k += 1
                
                if len(spans[k][1]) == 2:
                    upSpan = spans[k][0]
                    upSpanType = spans[k][1][0]

                    splitSpan = spans[k+1][0]
                    splitSpanType = spans[k+1][1][0]

                    split = upSpan.split(splitSpan)

                    if split[0]: otherSpans.append([split[0].strip(), [complSpanType, upSpanType, None]])
                    otherSpans.append([splitSpan, [complSpanType, upSpanType, splitSpanType]])
                    if split[1]: otherSpans.append([split[1].strip(), [complSpanType, upSpanType, None]])
                    # hier fehlt eins!
                    k += 2

            for span in otherSpans:
                print span

            splits = []          
            repl = ""
            for j in range(len(otherSpans)):
                span = otherSpans[j][0]
                if len(span) < 3:
                    output.append(otherSpans[j])
                    repl = repl + span
                else:
                    #print span
                    split = complSpan.split(span)
                    split = split[0]
                    #print split
                    #print repl
                    split = split.replace(repl, "") 
                    #print split
                    if not split:
                        output.append(otherSpans[j])
                        repl = repl + span
                    else:
                        output.append([split, [complSpanType, None, None]])
                        output.append(otherSpans[j])
                        repl = repl + split + span
            if split[1]: output.append([split[1], [complSpanType, None, None]])

            i = i + compl


    #for thing in output:
        #print thing




'''


    for i in range(len(spanList)):
        if len(spanList[i][1]) == 2:
            spanList[i][0] = spanList[i][0].replace(spanList[i+1][0], "")
            spanList[i+1][1]= [None] + spanList[i][1]
            spanList[i][1]= [None] + [spanList[i][1][0]] + [None]

#        if len(spanList[i][1]) > 2:
#            compl = len(spanList[i][1])
#            inter = range(1, compl)
#            print inter
#
#            for j in inter:
#                spanList[i][0] = spanList[i][0].replace(spanList[i+j][0], "")

    for item in spanList:
        print item


        text = []
        if partType[0] == "H": 
            continue
        else:
            words = part.split()
            for word in words:
                word = word.encode("utf-8")
                if partType[0] == "A2":
                    text.append([word, 'A1', 'A2', None])
                elif partType[0] == "A3":
                    text.append([word, 'A1', 'A2', 'A3'])
                else: 
                    text.append([word, partType[0], None, None])
        print text
'''   
