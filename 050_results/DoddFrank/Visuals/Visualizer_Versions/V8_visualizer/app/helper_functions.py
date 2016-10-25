import numpy


word_class = {'LogicalConnectors':'#8B69F9',
              'RegulatoryOperators':'#C25FF8',
              'EconomicOperands' : '#FFFF58',
              'Attributes': '#FFE258',
              'LegalReferences':'#AFAFAF',
              'FunctionWords':'#696969' ,
              'Other': '#A3A3A3',
              'white': 'white'}




def delete_white(words, colors):
    words_filtered=[]
    colors_filtered=[]
    remove_words = []
    for i in range(len(words)):
        if colors[i] != "white":
            words_filtered.append(words[i])
            colors_filtered.append(colors[i])
        else:
            remove_words.append(words[i])
    return words_filtered, colors_filtered, remove_words


def check_punctuation(word):
    if word[-1]=="." or word[-1]=="," or word[-1]==";"  or word[-1]=="'":
        word = word[:-1]
    if word[0]=="." or word[0]=="," or  word[0]==";" or word[-1]=="'":
        word = word[1:]
    return word



def sort_list_len(words, colors):
    words = numpy.array(words)
    colors = numpy.array(colors)
    index = [len(i) for i in words]
    index = numpy.array(index)
    index = index.argsort()
    sortedWords = words[index]
    sortedColors = colors[index]
    return sortedWords.tolist(), sortedColors.tolist()



def color_to_operand(colors):
    types = []
    word_color = dict((y,x) for x,y in word_class.iteritems())
    for element in colors:
        types.append(word_color[element])
    return types


def operand_to_color(types):
    colors = []
    for element in types:
        colors.append( word_class[element])
    return colors

