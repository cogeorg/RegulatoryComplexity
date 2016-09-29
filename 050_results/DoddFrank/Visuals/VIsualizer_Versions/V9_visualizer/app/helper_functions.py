import numpy
import os
import shutil


word_class = {'A-Antecedent':'#81fd81',
              'C-Consequent':'#cc99ff',
              'T1-Topic' : '#ffff99',
              'T2-Topic': '#ffff00',
              'T3-Topic':'#ffcc00',
              'EL-LeftEquivalent':'#d3d3d3' ,
              'ER-RightEquivalent': '#bababa',
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

# copy html files in personal folder
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

