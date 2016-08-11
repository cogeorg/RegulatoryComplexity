def format_list(aux_list):
    aux_list = aux_list.replace("\\","")
    aux_list = aux_list.replace(";","")
    aux_list = aux_list.split("],[")
    time_list, color_list, word_list, place_list = [], [], [], []
    for element in aux_list:
            aux = element.split('"')
            time_stamp = str(aux[4])
            if time_stamp in time_list:
                index = time_list.index(time_stamp)
                word_append = word_list[index]
                word_list[index] = word_append + "_" + str(aux[11])
                place_append = place_list[index]
                print place_append
                place_list[index] = place_append + "_" + str(aux[13])
            else:
                time_list.append(time_stamp)
                color_list.append(str(aux[6]))
                word_list.append(str(aux[11]))
                place_list.append(aux[13])
    return time_list, color_list, word_list, place_list


def check_proper_string(word, place):
    place_array = place.split("_")
    word_array = word.split("_")
    word_array = [x.strip() for (y,x) in sorted(zip(place_array,word_array))]
    word = " ".join(word_array)
    return word

def delete_white(words, colors):
    index = [i for i, v in enumerate(colors) if v == "white"]
    for i in index:
        colors.pop(i)
        words.pop(i)
    return words, colors

def color_to_operand(colors):
    dict = {'#554600':'GrammaticalOperators',
            '#806D15': 'LegalOperators',
            '#D4C26A': 'LegalReferences',
            '#FFF0AA': 'LogicalOperators',
            '#AA0739': 'RegulationOperators',
            'green': 'Attributes',
            'yellow': 'EconomicOperand' ,
            'red':'Other',
            'white': 'white'}
    types = []
    for element in colors:
        types.append( dict[element])
    return types


def operand_to_color(types):
    dict = {'GrammaticalOperators':'#554600',
            'LegalOperators':'#806D15',
             'LegalReferences':'#D4C26A',
            'LogicalOperators':'#FFF0AA' ,
             'RegulationOperators':'#AA0739',
             'Attributes': 'green',
             'EconomicOperand' : 'yellow',
            'Other': 'red',
            'white': 'white'}
    colors = []
    for element in types:
        colors.append( dict[element])
    return colors

