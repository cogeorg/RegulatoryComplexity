import string
import re


# Functions:
#           1) check_paragraph, check_number, check_upper, check_three_clause, check_four_clause,
#              check_five_clause, check_six_clause
#                       Args: Line  (string)
#                       Return: True/False (boolean)
#
#           2) check_sequence_paragraph, check_sequence_number, check_sequence_upper, check_sequence_clause
#                       Args: word/number, names, is_amended  (string, string list, boolean)
#                       Return: True/False (boolean)
#
#           3) check_h_i , check_same_sentence, check_sub_part, check_nothing
#           4) format_line, get_item, clean_note
#
#
# check_item are functions to identify if a line is an item or not.
# check_sequence_item are functions to identify if an item is in the sequence (besed in the previous items).
# check_others are helper functions to identify proper items.

# NOTE: for most of the item_type is necessarry to pass the three check functions


def check_paragraph(line):

    if len(line) < 5:
        return False
    elif line[0] == "(" and line[1].isalpha() and not (line[1].isupper()) and line[2] == ")" and \
            (line[4].isupper() or line[4] == "&" or len(re.findall(r'NOTE', line)) > 0) or line[4] == "[":
        return True
    else:
        return False


def check_number(line):

    if len(line) < 5:
        return False
    if (line[0] == "(" and line[1].isdigit() and line[2] == ")" and line[3] != ",") or \
            (line[0] == "(" and line[1].isdigit() and line[2].isdigit() and line[3] == ")" and line[4] != ","):
        return True
    else:
        return False


def check_upper(line):
    if line[0] == "(" and line[1].isalpha() and line[1].isupper() and line[2] == ")":
        return True
    else:
        return False


def check_three_clause(line):
    roman_list = ["i", "v", "x"]
    if line[0] == "(" and (line[1] in roman_list) and (line[2] in roman_list or line[2] == ")") and line[1].islower():
        return True
    else:
        return False


def check_four_clause(line):
    roman_list = ["I", "V", "X"]
    if line[0] == "(" and (line[1] in roman_list) and (line[2] in roman_list or line[2] == ")") and line[1].isupper():
        return True
    else:
        return False


def check_five_clause(line):
    if line[0] == "(" and line[1].isalpha() and line[1].islower() and line[2].isalpha() and line[2].islower() \
            and line[3] == ")" and line[1] != "i":
        return True
    else:
        return False


def check_six_clause(line):
    if line[0] == "(" and line[1].isalpha() and line[1].isupper() and line[2].isalpha() and line[2].isupper() \
            and line[3] == ")":
        return True
    else:
        return False





def check_sequence_paragraph(word, names, is_amended):
    if names == []:
        if word[1] == 'a':
            return True
        else:
            if is_amended:
                return True
            else:
                return False
    else:
        name = names[-1]
        list_word = list(string.ascii_lowercase)
        i = 0
        for element in list_word:
            if element == name[1]:
                break
            i += 1
        return word[1] == list_word[i + 1]


def check_sequence_upper(word, names, is_amended):

    if names == []:
        if word[1] == 'A':
            return True
        else:
            if is_amended:
                return True
            else:
                return False
    else:
        name = names[-1]
        list_word = list(string.ascii_lowercase)
        i = 0
        for element in list_word:
            if element.upper() == name[1]:
                break
            i += 1
        return word[1] == list_word[i + 1].upper()



def check_sequence_numbers(number, names, is_amended):
    if names == []:
        if number[1] == '1' or is_amended:
            return True
        else:
            return False
    else:
        number = float(get_item(number))
        number_aux = float(get_item(names[-1])) + 1
        return number == number_aux


def check_sequence_clause(line, names, is_amended):
    if names == []:
        if line[1] == 'i':
            return True
        else:
            if is_amended:
                return True
            else:
                return False
    else:

        actual_clause = get_item(line)
        last_clause = get_item(names[-1])

        list_roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
                      'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx']
        i = 0
        for element in list_roman:
            if element == last_clause:
                break
            i += 1
        return actual_clause == list_roman[i + 1]




def check_h_i(line, line_list):
    if len(line_list) > 0 and line[1].lower() == "i":
        line = line_list[-1].strip()
        if line[-1] == "-" or line[-1] == ":":
            return False
        else:
            return True
    else:
        return True


def check_same_sentence(line):
    aux_list = line.split(" ")
    aux_list = filter(lambda x: not re.match(r'^\s*$', x), aux_list)
    false_list = ["paragraph", "clause", "paragraphs", "section", "sections", "Clause",
                  "clause", "subparagraph", "subclause", "subsection"]
    false_list_2 = [","]

    if len(aux_list) > 0 and (aux_list[-1] in false_list or aux_list[-1][-1] in false_list_2):
        return True
    else:
        return False


def check_sub_part(line):
    if line[:9] == "Subtitle " or line[:5] == "PART ":
        return True
    else:
        return False


def check_nothing(line):
    return False

# Other functions


def format_line(line):
    line_aux = re.sub("  ", " ", line)
    line_aux = line_aux.replace("\n", "")
    return line_aux


def get_item(line):
    line = line.split(")")
    line = line[0]
    index = -len(line) + 1
    return line[index:]


def clean_note(note):
    cleaned_note = re.sub(";NOTE", '', note)
    cleaned_note = re.sub(":", "", cleaned_note)
    return cleaned_note.strip()
