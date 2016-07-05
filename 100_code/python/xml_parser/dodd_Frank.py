import string


#Basic functions to check:

def check_sequence(letter, names):
    """Check if the paragraph found is sequence of the last
    Args:
        letter (string): paragraph found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """
    if names==[]:
        if letter[1]=='a':
            return True
        else:
            return False
    else:
        name=names[-1]
        list_letter = list(string.ascii_lowercase)
        i=0
        for element in list_letter:
            if element == name[1]:
                break
            i+=1
        return letter[1] == list_letter[i+1]

def check_sequence_upper(letter, names):
    """Check if the bullet found is sequence of the last
    Args:
        letter (string): bullet found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """
    if names==[]:
        if letter[1]=='A':
            return True
        else:
            return False
    else:
        name=names[-1]
        list_letter = list(string.ascii_lowercase)
        i=0
        for element in list_letter:
            if element.upper() == name[1]:
                break
            i+=1
        return letter[1] == list_letter[i+1].upper()

def check_sequence_numbers(number, names):
    """Check if the bullet found is sequence of the last

    Args:
        number (string): Section found.
        names (list of string): list of the paragraph names .

    Returns:
        Boolean: True/False
        """

    if number[-1]==")":
        number=float(number[1:-1])
    else:
        number=float(number[1:-2])
    if names==[]:
        if number==1:
            return True
        else:
            return False
    else:
        number_aux=names[-1]
        if number_aux[3]==")":
            number_aux=float(number_aux[1:3])+1
        else:
            number_aux=float(number_aux[1])+1
        return number == number_aux

def check_paragraph(line):
    """Check if the line is a paragraph

    Args:
        line (string): line of the text

    Returns:
        Boolean: True/False
        """

    if line[0]=="(" and line[1].isalpha() and not(line[1].isupper()) and line[2]==")":
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

    if line[0]=="(" and line[1].isdigit() and line[2]==")" and line[3]==" ":
        return True
    else:
        return False

def check_clause(line):
    if line[0]=="(" and (line[1]=="i" or line[1]=="v" or line[1]=="x"):
        return True
    else:
        return False

def check_upper(line):
    if line[0]=="(" and line[1].isalpha() and line[1].isupper() and line[2]==")":
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
    lines_list=[]
    list_delete=['[[Page 124','']
    flag = False
    with open(file_name) as f:
        for line in f:
            line_aux=line.decode('utf-8').strip()
            if line[:9]== "TITLE I--" : flag= True         #Start to store since TITLE I, flag=True
            if line_aux[:10] not in list_delete and flag:
                lines_list.append(line_aux)
    return lines_list




def find_title(line_list):
    """Finds the number of Titles from the list of lines. It creates two different
    lists. The elements of the list are: 1) Name of the title 2) List containing the
    Text inside of the title.

    The code checks for each line:
        if line is ***title*** then append the line to the list of names (1)
        if line is ***SEC or Subtitle or Part*** then append the line to the Text (2)
                        ---The next element of a title is a section, Subtitle or Part---
            if line is ***part of a new title*** then create a new list and append line
            if line is ***part of an old title*** then append line
        if line is ***part of the title name*** then concatenate the line to the
                last element of the list.

    Important variables:
        flag_new_section (Boolean):
            if False then next SEC/Subtittle/Part is a part of the new Title
            if True then next SEC/Subtittle/Part is a part of the old Title

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
        if line[:5] == "TITLE":
            names.append(line)              #list of titles.
            flag_new_sec = True
            if len(list_aux) >0:            #Append the list of text related to the last title
                lines_section.append(list_aux)
        if line[:4] == "SEC." or line[:8] == "Subtitle" or line[:4]=="PART":
            if flag_new_sec:                #Part of the new title
                list_aux=[]
                list_aux.append(line)
                flag_new_sec=False
            else:                           #Part of the old title
                list_aux.append(line)
                flag_new_sec=False
        elif flag_new_sec:                  #Not a new section, then it is part of the title name
                names[-1] = names[-1] + " " + line
        else:                               #Not a new section or old section or part of the title name
            list_aux.append(line)
    if len(list_aux) >0:                    #Append the list of text related to the last title
        lines_section.append(list_aux)
    return names, lines_section


def find_subtitle(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec, flag_subtitle = False, False
    for line in line_list:
        if line[:9] == "Subtitle ":
            names.append(line)
            flag_new_sec = True
            flag_subtitle=True
            if len(list_aux) >0:
                lines_section.append(list_aux)
        if flag_subtitle:
            if line[:4] == "SEC." or line[:5]=="PART ":
                if flag_new_sec:
                    list_aux=[]
                    list_aux.append(line)
                    flag_new_sec=False
                else:
                    list_aux.append(line)
                    flag_new_sec=False
            elif flag_new_sec:
                    names[-1] = names[-1] + " " + line
            else:
                list_aux.append(line)
    if len(list_aux) >0:
        lines_section.append(list_aux)
    if len(names)>len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_part(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec, flag_subtitle = False, False
    for line in line_list:
        if line[:5] == "PART":
            names.append(line)
            flag_new_sec = True
            flag_subtitle=True
            if len(list_aux) >0:
                lines_section.append(list_aux)
        if flag_subtitle:
            if line[:4] == "SEC.":
                if flag_new_sec:
                    list_aux=[]
                    list_aux.append(line)
                    flag_new_sec=False
                else:
                    list_aux.append(line)
                    flag_new_sec=False
            elif flag_new_sec:
                    names[-1] = names[-1] + " " + line
            else:
                list_aux.append(line)
    if len(list_aux) >0:
        lines_section.append(list_aux)
    if len(names)>len(lines_section):    #Text for the last title
        lines_section.append([])
    return names, lines_section


def find_sec(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if line[:9] == "Subtitle " or line[:5]=="PART ":
            break
        if line[:4] == "SEC.":
            names.append(line)
            flag_new_sec = True
            if len(list_aux) >0:
                lines_section.append(list_aux)
            if len(names)>len(lines_section)+1:
                lines_section.append([])
        elif check_paragraph(line) or check_number(line):
            if flag_new_sec:
                list_aux=[]
                list_aux.append(line)
                flag_new_sec=False
            else:
                list_aux.append(line)
                flag_new_sec=False
        elif flag_new_sec:
                names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(list_aux) >0:
        lines_section.append(list_aux)
    if len(names)>len(lines_section):
        lines_section.append([])
    return names, lines_section


def find_paragraph(line_list):
    names, list_aux, lines_section = [], [], []
    flag_new_sec = False
    for line in line_list:
        if check_paragraph(line):
            if check_sequence(line[:3],names):
                names.append(line)
                flag_new_sec = True
                if len(list_aux) >0:
                    lines_section.append(list_aux)
        elif check_number(line):
            if flag_new_sec:
                list_aux=[]
                list_aux.append(line)
                flag_new_sec=False
            else:
                list_aux.append(line)
                flag_new_sec=False
        elif flag_new_sec:
                names[-1] = names[-1] + " " + line
        else:
            list_aux.append(line)
    if len(names)==len(lines_section)+1:
        lines_section.append([])
    return names, lines_section






