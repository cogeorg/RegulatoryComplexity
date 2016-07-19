from item_functions import *
import re


# Functions:
#           1) get_line_list
#           2) find_item
#           3) find_amended_item


def get_line_list(file_name):
    """Gets the list of the cleaned lines from the input file.
    It starts to store the lines since the first Title (Not index)

    Args:
        file_name (string): The directory of the file.

    Returns:
        lines_list: List of lines .
        """
    lines_list = []
    list_delete = ['[[Page 124']                              # Head of the source file pages
    flag = False
    last_line = "last"                                        # Auxiliar variable to store the last line
    with open(file_name) as f:
        for line in f:
            if re.match(r'^\s*$', line) is None:              # Filter empty lines (one or more spaces \s)
                line_aux = line.decode('utf-8').strip()       # Strip line
                if line[:9] == "TITLE I--":                   # Start to store from TITLE I, flag=True
                    flag = True
                if line_aux[:10] not in list_delete and flag:   # Filter line representing the head of the source file
                    if check_same_sentence(last_line):          # Function to check if is a line continuation
                        lines_list[-1] = lines_list[-1] + " " + line_aux  # if line continuation append to the last line
                    else:
                        lines_list.append(format_line(line_aux))   # if not a line cont. append to the list.
                last_line = line_aux
    return lines_list



def find_item(line_list, is_amended, item_type):
    """Find_item is a "switch/case" function which finds the number of elements depending
    the item_type.

    It creates two different lists.
        1) The first list is called names, which represents the names of the items.

        2) The second list is called lines_section, which represents the body of the item.

        For example: TITLE I FINANCIAL STABILITY (Name)
                     SEC 1. Short Title          (Body)
                     SEC 2. Definitions          (Body)
                     ....

    The code checks for each line:
        Case 1) line is an item  (name)
        Case 2) line is a child or descendant. (body)
        Case 3) line is part of the item name. (name)
        Case 4) line is part of the child/descendant. (body)

    Args:
        lines_list (string list): The cleaned list of lines from get_line_list.
        is_amended (boolean): True if you are looking for amended types/ False otherwise.
        item_type (string): Name of the item type that you want to find.

    Returns:
        names: List of item's names.
        lines_section: List of lists. Each nested list is linked to each item.
        """

    names, list_aux, lines_section = [], [], []
    flag_new_item = False                            # Flag representing a new item.
    flag_start_point = False                            # Flag representing the starting point. Algorithm starts to _
    is_item_child = get_checker_functions(item_type)    # store lines when is found an item type. (Cond 1)
    for line in line_list:
        if len(is_item_child) == 3:                  # Necessary for the item "section".
            if is_item_child[2](line):
                break
        if is_item_child[0](line, names, is_amended, list_aux):  # List of functions representing the necessary _
            names.append(line)                                   # conditions to be an item. (Cond 1)
            flag_new_item, flag_start_point = True, True         # New Item and start point.
            if len(list_aux) > 0:
                lines_section.append(list_aux)                   # Line belonging to the old item.
                list_aux = []                                    # Restart line_aux for the new item
            if len(names) > len(lines_section) + 1:              # In the case there is no body in the item _
                lines_section.append([])                         # append an empty list.
        elif flag_start_point:
            if is_item_child[1](line):                           # List of function representing the necessary _
                if flag_new_item:                                # conditions to be a child (Cond 2)
                    list_aux = []
                    list_aux.append(line)                        # Append line to the list_aux, representing the body
                    flag_new_item = False                        # Set flag new item as false
                else:
                    list_aux.append(line)                        # Old element then append line to the old list
            elif flag_new_item:
                names[-1] = names[-1] + " " + line               # Part of the item name (Cond 3)
            else:
                list_aux.append(line)                            # Part of the child/descendant (Cond 4)
    if len(list_aux) > 0:                                        # Line belonging to the old item.
        lines_section.append(list_aux)
    if len(names) > len(lines_section):                          # In the case there is no body in the item
        lines_section.append([])
    return names, lines_section


def find_amended_item(text):
    """Find_amended is a function which finds the amended elements.
    Args:
        text (string): Text of the node

    Returns:
        amended_text: amended text of the node.
        """

    if len(re.findall(r"``SEC\.(.*?)''\.", text)) > 0:          # Find amended item of the form ``SEC. ... ''.
        amended_text = re.findall(r"``SEC\.(.*?)''\.", text)
        amended_text = "``SEC." + amended_text[0] + "''."
    elif len(re.findall(r"``SEC\.(.*?)''\;\sand", text)) > 0:   # Find amended item of the form ``SEC. ... ''; and
        amended_text = re.findall(r"``SEC\.(.*?)''\;\sand", text)
        amended_text = "``SEC." + amended_text[0] + "''; and"
    elif len(re.findall(r"``SEC\.(.*?)''\;", text)) > 0:        # Find amended item of the form ``SEC. ... '';
        amended_text = re.findall(r"``SEC\.(.*?)''\;", text)
        amended_text = "``SEC." + amended_text[0] + "'';"
    elif len(re.findall(r"``\((.*?)''\.", text)) > 0:           # Find amended item of the form ``([A-Z0-9] ... ''.
        amended_text = re.findall(r"``\((.*?)''\.", text)
        if len(re.findall(r"``\((.*?)''\.", text)) > 1:
            amended_text = "``(" + amended_text[0] + "''. " + "``(" + amended_text[1] + "''."   # Typo Dodd-Frank
        else:
            amended_text = "``(" + amended_text[0] + "''."
    elif len(re.findall(r"``\((.*?)''\;\sand", text)) > 0:      # Find amended item of the form ``([A-Z0-9] ... ''; and
        amended_text = re.findall(r"``\((.*?)''\;\sand", text)
        amended_text = "``(" + amended_text[0] + "''; and"
    elif len(re.findall(r"``\((.*?)''\;", text)) > 0:           # Find amended item of the form ``([A-Z0-9] ... '';
        amended_text = re.findall(r"``\((.*?)''\;", text)
        amended_text = "``(" + amended_text[0] + "'';"
    else:
        amended_text = ""
    return amended_text




