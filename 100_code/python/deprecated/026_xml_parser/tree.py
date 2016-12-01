from dodd_frank import *
import re
import xml.etree.ElementTree as eT


# Funtions:
#          1) build_item
#          2) build_amended_item



def build_item(line_list, node, is_amended, item_type):
    """ build_item is a recursive function. It builds the nodes of
    the tree depending the item_type (see Readme).


    Args:
        line_list (string list): The list of lines in the input text.
        node (object): Parent node in the tree structure.
        is_amended (boolean): True if the item is an amended section.
        item_type (string): Type of the item (child) to be built

    Returns:
        element_not_empty (boolean): True if there are items (children) in the section
                                     False if there is no node in the section

    Important functions:
        find_item: get the items and the inner text for each item type
        get_list_levels: get the list of descendant items
          """
    items, lines_item = find_item(line_list, is_amended, item_type)  # Get the items and the inner text
    i = 0                                                         # Variable to iterate in the lines_item
    element_not_empty = False                                     # Variable representing if the elements are not null
    for item in items:
        item_node = eT.SubElement(node, item_type)                # Create the node for each item
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', item)          # Find all the notes in the item
        aux_text = item                                           # Variable to manipulate the item
        for note in notes:
            item_node.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))  # Create the "Notes" attribute
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", ' ', aux_text)    # Delete the note's text from the item
        if is_amended:
            aux_text = "``" + aux_text                            # Amended items must be preceded by ``
        item_node.text = aux_text                                 # Insert the item to the node
        for item_level in get_list_levels(item_type):
            if item_type in ['title', 'subtitle', 'part']:        # These items have known descendants, visit each one.
                build_item(lines_item[i], item_node, is_amended, item_level)
            elif build_item(lines_item[i], item_node, is_amended, item_level):  # Other items have unknown descendants
                break                                           # Visit all the descendants until  ->
        i += 1                                                  # you find the next not empty
        element_not_empty = True                                # Items are not empty
    return element_not_empty



def build_amended_item(node):
    """ build_amended_item is a recursive function. It builds the nodes for the
    amended items.


    Args:
        node (object): Parent node in the tree structure.

    Returns:
        element_not_empty (boolean): True if there are items (children) in the section
                                     False if there is no node in the section

    Important functions:
        find_amended_item: get the items and the inner text for each amended item type
          """
    string_aux = str(node.text)                                 # Get the text from the node
    amended_text = find_amended_item(string_aux)                # Find the amended text in the node
    if amended_text != "":
        list_lines_amended = re.split(r"``", amended_text)      # Split the text to get the amended items
        list_lines_amended = filter(lambda x: not re.match(r'^\s*$', x), list_lines_amended)    # Drop empty elements
        list_lines_amended = [x.strip() for x in list_lines_amended]
        amended_type = get_amended_item(list_lines_amended[0])  # Get the item's amended type
        if amended_type:
            build_item(list_lines_amended, node, True, amended_type)  # Build the amended node
            string_aux = string_aux.replace(amended_text, "")   # Delete amended text from the no amended node
            node.text = string_aux                              # Set new text (without amended) to the node
    return True


