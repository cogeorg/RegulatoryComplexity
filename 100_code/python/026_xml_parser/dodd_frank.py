import string
import re


# Functions:
#   Main function: find_title, find_section, find_subtitle, find_part, find_bullet, find_subbullet, find_third_bullet
#   Simple functions: check_sequence, check_paragraphs, check_sequence_numbers, check_sequence_upper, check_number,
#                       check_upper, clean_note.


def check_sequence(letter, names):
    """Check if the paragraph found is sequence of the last
    Args:
        letter (string): paragraph found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """
    if names == []:
        if letter[1] == 'a':
            return True
        else:
            return False
    else:
        name = names[-1]
        list_letter = list(string.ascii_lowercase)
        i = 0
        for element in list_letter:
            if element == name[1]:
                break
            i += 1
        return letter[1] == list_letter[i + 1]


def check_sequence_upper(letter, names):
    """Check if the bullet found is sequence of the last
    Args:
        letter (string): bullet found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """
    if names == []:
        if letter[1] == 'A':
            return True
        else:
            return False
    else:
        name = names[-1]
        list_letter = list(string.ascii_lowercase)
        i = 0
        for element in list_letter:
            if element.upper() == name[1]:
                break
            i += 1
        return letter[1] == list_letter[i + 1].upper()


def check_sequence_numbers(number, names):
    """Check if the bullet found is sequence of the last

    Args:
        number (string): Section found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """

    if number[-1] == ")":
        number = float(number[1:-1])
    else:
        number = float(number[1:-2])
    if names == []:
        if number == 1:
            return True
        else:
            return False
    else:
        number_aux = names[-1]
        if number_aux[3] == ")":
            number_aux = float(number_aux[1:3]) + 1
        else:
            number_aux = float(number_aux[1]) + 1
        return number == number_aux


def check_paragraph(line):
    """Check if the line is a paragraph

    Args:
        line (string): line of the text

    Returns:
        Boolean: True/False
        """

    if len(line) < 5:
        return False
    elif line[0] == "(" and line[1].isalpha() and not (line[1].isupper()) and line[2] == ")" and \
            (line[4].isupper() or line[4] == "&"):
        return True
    else:
        return False


def check_number(line):
    """Check if the line is a bullet

    Args:
        line (string): line of the text

    Returns:
        Boolean: True/False
        """

    if line[0] == "(" and line[1].isdigit() and line[2] == ")" and line[3] == " " or \
            (line[0] == "(" and line[1].isdigit() and line[2].isdigit() and line[3] == ")" and line[4] == " "):
        return True
    else:
        return False


def check_clause(line):
    roman_list = ["i", "v", "x"]
    if line[0] == "(" and (line[1] in roman_list) and (line[2] in roman_list or line[2] == ")") and line[1].islower():
        return True
    else:
        return False


def check_upper(line):
    if line[0] == "(" and line[1].isalpha() and line[1].isupper() and line[2] == ")":
        return True
    else:
        return False


def check_h_i(line_list):
    if len(line_list) > 0:
        line = line_list[-1]
        if line[-1] == "-":
            return False
        else:
            return True
    else:
        return True


def check_proper_upper(line):
    if line[:2] == "(A":
        return True
    else:
        return False


def get_line_list(file_name):
    """Gets the list of the cleaned lines from the input file.
    It starts to store the lines since the first Title (Not index)

    Args:
        file_name (string): The directory of the file.

    Returns:
        lines_list: List of lines .
        """
    lines_list = []
    list_delete = ['[[Page 124', '']
    flag = False
    with open(file_name) as f:
        for line in f:
            line_aux = line.decode('utf-8').strip()
            if line[:9] == "TITLE I--":
                flag = True  # Start to store since TITLE I, flag=True
            if line_aux[:10] not in list_delete and flag:
                lines_list.append(line_aux)
    return lines_list


def find_title(line_list):
    """Finds the number of Titles from the list of lines. It creates two different
    lists.
        1) The first list is called names. Each element of the list is the name of the title

        2) The second list is called lines_section. Each element of the list is a list which
        represents the text of the child body (SEC/Subtitle/Part)


    The code checks for each line:
        Case 1) line is the head of the title then append the line to the list of names (1)

        Case 2) line is the head of the child (SEC/Subtitle/Part) then
            append the line to the Text list (2).

        Case 3) line is part of the title name then append the line to the name of
         the title

        Case 4) line is part of the SEC/Subtitle/Part body


    Important variables:
        flag_new_section (Boolean):
            False then next SEC/Subtittle/Part is part of the new Title
            True then next SEC/Subtittle/Part is  part of the old Title

        note: It is also useful to identify lines which are part of the title name

    Args:
        lines_section (string): The cleaned list of lines from get_line_list.

    Returns:
        names: List of the TITLE names.
        lines_section: Nested lists of lines for each title
        """
    names, list_aux, lines_section = [], [], []
    flag_new_sec = True
    for line in line_list:
        if line[:5] == "TITLE":     # Case 1
            names.append(line)      # list of titles.
            flag_new_sec = True     # New title: True
            if len(list_aux) > 0:   # Append the list of text related to the last title if it exists
                lines_section.append(list_aux)
        if line[:4] == "SEC." or line[:8] == "Subtitle" or line[:4] == "PART":  # Case 2)
            if flag_new_sec:        # New title
                list_aux = []       # New list of text
                list_aux.append(line)   # Append "SEC/Subititle/Part" first line to the new list
                flag_new_sec = False
            else:                   # Actual title
                list_aux.append(line)  # Append "SEC/Subititle/Part" first line to the actual list.
                flag_new_sec = False
        elif flag_new_sec:          # Case 3
            names[-1] = names[-1] + " " + line
        else:                       # Case 4
            list_aux.append(line)
    if len(list_aux) > 0:           # Append the list of text related to the last title
        lines_section.append(list_aux) # Append to the list of list
    return names, lines_section


def find_subtitle(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec, flag_subtitle = False, False
    for line in line_list:
        if line[:9] == "Subtitle ":
            names.append(line)
            flag_new_sec = True
            flag_subtitle = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
        elif flag_subtitle:
            if line[:4] == "SEC." or line[:5] == "PART ":
                if flag_new_sec:
                    list_aux = []
                    list_aux.append(line)
                    flag_new_sec = False
                else:
                    list_aux.append(line)
                    flag_new_sec = False
            elif flag_new_sec:
                names[-1] = names[-1] + " " + line
            else:
                list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_part(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec, flag_part = False, False
    for line in line_list:
        if line[:5] == "PART ":
            names.append(line)
            flag_new_sec = True
            flag_part = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
        elif flag_part:
            if line[:4] == "SEC.":
                if flag_new_sec:
                    list_aux = []
                    list_aux.append(line)
                    flag_new_sec = False
                else:
                    list_aux.append(line)
                    flag_new_sec = False
            elif flag_new_sec:
                names[-1] = names[-1] + " " + line
            else:
                list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):  # Text for the last title
        lines_section.append([])
    return names, lines_section


def find_sec(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if line[:9] == "Subtitle " or line[:5] == "PART ":
            break
        if line[:4] == "SEC.":
            names.append(line)
            flag_new_sec = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
                list_aux = []
            if len(names) > len(lines_section) + 1:
                lines_section.append([])
        elif check_paragraph(line) or check_number(line):
            if flag_new_sec:
                list_aux = []
                list_aux.append(line)
                flag_new_sec = False
            else:
                list_aux.append(line)
                flag_new_sec = False
        elif flag_new_sec:
            names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_paragraph(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if check_paragraph(line) and check_sequence(line[:3], names) and check_h_i(list_aux):
            names.append(line)
            flag_new_sec = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
                list_aux = []
            if len(names) > len(lines_section) + 1:
                lines_section.append([])
        elif check_number(line):
            if flag_new_sec:
                list_aux = []
                list_aux.append(line)
                flag_new_sec = False
            else:
                list_aux.append(line)
                flag_new_sec = False
        elif flag_new_sec:
            names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_bullet(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if check_number(line):
            if check_sequence_numbers(line[:4], names):
                names.append(line)
                flag_new_sec = True
                if len(list_aux) > 0:
                    lines_section.append(list_aux)
                    list_aux = []
                if len(names) > len(lines_section) + 1:
                    lines_section.append([])
        elif check_upper(line) and check_proper_upper(line):
            if flag_new_sec:
                list_aux = []
                list_aux.append(line)
                flag_new_sec = False
            else:
                list_aux.append(line)
                flag_new_sec = False
        elif flag_new_sec:
            names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_sub_bullet(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if check_upper(line) and check_sequence_upper(line[:3], names):
            names.append(line)
            flag_new_sec = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
                list_aux = []
            if len(names) > len(lines_section) + 1:
                lines_section.append([])
        elif check_clause(line):
            if flag_new_sec:
                list_aux = []
                list_aux.append(line)
                flag_new_sec = False
            else:
                list_aux.append(line)
                flag_new_sec = False
        elif flag_new_sec:
            names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_third_bullet(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if check_clause(line):
            names.append(line)
            flag_new_sec = True
            if len(list_aux) > 0:
                lines_section.append(list_aux)
                list_aux = []
            if len(names) > len(lines_section) + 1:
                lines_section.append([])
            if flag_new_sec:
                list_aux = []
                list_aux.append(line)
                flag_new_sec = False
            else:
                list_aux.append(line)
                flag_new_sec = False
        elif flag_new_sec:
            names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) > 0:
        lines_section.append(list_aux)
    if len(names) > len(lines_section):
        lines_section.append([])
    return names, lines_section


# Other functions
def clean_note(note):
    cleaned_note = re.sub(";NOTE", '', note)
    cleaned_note = re.sub(":", "", cleaned_note)
    return cleaned_note.strip()


