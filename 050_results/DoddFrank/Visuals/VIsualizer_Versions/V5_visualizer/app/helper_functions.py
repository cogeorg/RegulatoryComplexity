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
