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

    
    output = []
    i = 0
    while i < len(spanList)-1:
        if len(spanList[i][1]) == 1:
            output.append([spanList[i][0], spanList[i][1] + [None, None]])
            i += 1
        if len(spanList[i][1]) > 1:
            compl = len(spanList[i][1])
            inter = range(1, compl)




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
