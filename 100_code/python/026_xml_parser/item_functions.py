from checkers import *

# Functions:
#           1) is_title, is_part, is_subtitle, is_section, is_paragraph, is_bullet, is_two_bullet,
#              is_three_bullet, is_four_bullet, is_five_bullet, is_six_bullet, is_part_sec_sub,
#              is_par_num
#                       Args: *params  (list of parameters)
#                       Return: True/False (boolean)
#
#           2) get_amended_item, get_list_levels, get_checker_functions
#                       Args: item (line, item_type)  (string)
#                       Return: list (string list/ function list)
#
#
# is_item are functions that join the checker functions depending of the item_type (check_item, check_sequence, ...).
# get_something are functions which returns a proper list of elements or functions depending of the item_type
# (see Readme).



def is_title(*params):
    # line, names, is_amended, list_aux
    if params[0][:5] == "TITLE":
        return True
    else:
        return False


def is_part(*params):
    if params[0][:5] == "PART ":
        return True
    else:
        return False


def is_subtitle(*params):
    if params[0][:9] == "Subtitle ":
        return True
    else:
        return False


def is_section(*params):
    if params[0][:4] == "SEC.":
        return True
    else:
        return False



def is_paragraph(*params):
    # line, names, is_amended, list_aux
    if check_paragraph(params[0]) and check_sequence_paragraph(params[0], params[1], params[2]) \
            and check_h_i(params[0], params[3]):
        return True
    else:
        return False


def is_bullet(*params):
    if check_number(params[0]) and check_sequence_numbers(params[0], params[1], params[2]):
        return True
    else:
        return False


def is_two_bullet(*params):
    if check_upper(params[0]) and check_sequence_upper(params[0], params[1], params[2]) \
            and check_h_i(params[0], params[3]):
        return True
    else:
        return False


def is_three_bullet(*params):
    if check_three_clause(params[0]) and check_sequence_clause(params[0], params[1], params[2]):
        return True
    else:
        return False



def is_four_bullet(*params):
    if check_four_clause(params[0]):
        return True
    else:
        return False


def is_five_bullet(*params):
    if check_five_clause(params[0]):
        return True
    else:
        return False


def is_six_bullet(*params):
    if check_six_clause(params[0]):
        return True
    else:
        return False




def is_part_sec(*params):
    if params[0][:4] == "SEC." or params[0][:5] == "PART ":
        return True
    else:
        return False


def is_part_sec_sub(*params):
    if params[0][:4] == "SEC." or params[0][:5] == "PART " or params[0][:9] == "Subtitle ":
        return True
    else:
        return False


def is_par_num(*params):
    if check_paragraph(params[0]) or check_number(params[0]):
        return True
    else:
        return False


def get_amended_item(line):
    if is_section(line):
        return "section"
    elif check_paragraph(line):
        return "paragraph"
    elif check_number(line):
        return "bullet"
    elif check_upper(line):
        return "two_bullet"
    elif check_three_clause(line):
        return "three_bullet"
    elif check_four_clause(line):
        return "four_bullet"
    elif check_five_clause(line):
        return "amended_par"
    else:
        return False


def get_list_levels(item_type):
    if item_type == "title":
        return ["section", "subtitle"]
    elif item_type == "part":
        return ["section"]
    elif item_type == "subtitle":
        return ["section", "part"]
    elif item_type == "section":
        return ["paragraph", "bullet", "two_bullet", "three_bullet"]
    elif item_type == "paragraph":
        return ["bullet", "two_bullet", "three_bullet"]
    elif item_type == "bullet":
        return ["two_bullet", "three_bullet"]
    elif item_type == "two_bullet":
        return ["three_bullet"]
    elif item_type == "three_bullet":
        return ["four_bullet"]
    elif item_type == "four_bullet":
        return ["five_bullet"]
    elif item_type == "five_bullet":
        return ["six_bullet"]
    elif item_type == "amended_par":
        return ["bullet"]
    else:
        return ""



def get_checker_functions(item):
    if item == "title":
        is_item_child = [is_title, is_part_sec_sub]
    elif item == "subtitle":
        is_item_child = [is_subtitle, is_part_sec]
    elif item == "part":
        is_item_child = [is_part, is_section]
    elif item == "section":
        is_item_child = [is_section, is_par_num, check_sub_part]
    elif item == "paragraph":
        is_item_child = [is_paragraph, check_number]
    elif item == "bullet":
        is_item_child = [is_bullet, check_upper]
    elif item == "two_bullet":
        is_item_child = [is_two_bullet, check_three_clause]
    elif item == "three_bullet":
        is_item_child = [is_three_bullet, check_four_clause]
    elif item == "four_bullet":
        is_item_child = [is_four_bullet, check_five_clause]
    elif item == "five_bullet":
        is_item_child = [is_five_bullet, check_six_clause]
    elif item == "six_bullet":
        is_item_child = [is_six_bullet, check_nothing]
    elif item == "amended_par":
        is_item_child = [is_five_bullet, check_number]
    else:
        is_item_child = "", ""
    return is_item_child

