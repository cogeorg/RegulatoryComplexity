from dodd_frank import get_line_list, find_title, find_subtitle, find_part, find_sec, find_paragraph, clean_note, \
    find_bullet, find_sub_bullet, find_third_bullet
import re
import xml.etree.ElementTree as eT


# Funtions: build_title, build_section, build_subtitle, build_part, build_bullet, build_subbullet, build_
# All the functions with similar structure to build_title

def build_title(line_list, node):
    """Builds the first level of the tree: Titles.
    Creates a section for each Title found in the text and
    calls the proper function to build the child nodes iteratively.

    Args:
        line_list (string list): The list of lines in the input text.
        node (object): Parent node in the tree structure.

    Returns:
        element_not_empty (boolean): True if there are nodes in the section
                                     False if there is no node in the section
          """

    children, lines_section = find_title(line_list)
    i = 0  # Varibale to get the element from lines_section
    for child in children:
        title = eT.SubElement(node, "Title")  # Create the subElement Title (parent:Regulation)
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)  # Find all the notes in the Section
        aux_text = child                       # Auxiliar variable to clean the text
        for note in notes:
            title.set('Notes', clean_note(note))  # Create the "Notes" attribute
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              ' ', aux_text)  # Variable name of the title without Notes
        title.text = aux_text
        build_section(lines_section[i], title)  # Build section nodes
        build_subtitle(lines_section[i], title)  # Build subtitle nodes
        i += 1
    return True


def build_subtitle(line_list, node):
    children, lines_subtitle = find_subtitle(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        subtitle = eT.SubElement(node, "Subtitle")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            subtitle.set('Notes', clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              ' ', aux_text)
        subtitle.text = aux_text
        # both because the structure
        build_section(lines_subtitle[i], subtitle)
        build_part(lines_subtitle[i], subtitle)
        element_not_empty = True
        i += 1
    return element_not_empty


def build_part(line_list, node):
    children, lines_part = find_part(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        part = eT.SubElement(node, "Part")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            part.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              ' ', aux_text)
        part.text = aux_text
        build_section(lines_part[i], part)
        element_not_empty = True
        i += 1
    return element_not_empty


def build_section(line_list, node):
    children, lines_section = find_sec(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        section = eT.SubElement(node, "Section")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            section.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              ' ', aux_text)
        section.text = aux_text
        element_not_empty = True

        # Build all the child nodes. The structure is different for each section
        if build_paragraph(lines_section[i], section):
            pass
        elif build_bullet(lines_section[i], section):
            pass
        elif build_sub_bullet(lines_section[i], section):
            pass
        elif build_third_bullet(lines_section[i], section):
            pass
        i += 1
    return element_not_empty


def build_paragraph(line_list, node):
    children, lines_paragraph = find_paragraph(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        paragraph = eT.SubElement(node, "Paragraph")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            paragraph.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", ' ', aux_text)
        paragraph.text = aux_text

        # Build all the child nodes. The structure is different for each paragraph
        if build_bullet(lines_paragraph[i], paragraph):
            pass
        elif build_sub_bullet(lines_paragraph[i], paragraph):
            pass
        elif build_third_bullet(lines_paragraph[i], paragraph):
            pass
        i += 1
        element_not_empty = True
    return element_not_empty


def build_bullet(line_list, node):
    children, lines_bullet = find_bullet(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        bullet = eT.SubElement(node, "Bullet")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            bullet.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", ' ', aux_text)
        bullet.text = aux_text
        # Build all the child nodes. The structure is different for each bullet
        if build_sub_bullet(lines_bullet[i], bullet):
            pass
        else:
            build_third_bullet(lines_bullet[i], bullet)
        element_not_empty = True
        i += 1
    return element_not_empty


def build_sub_bullet(line_list, node):
    children, lines_sub_bullet = find_sub_bullet(line_list)
    i = 0
    element_not_empty = False
    for child in children:
        subbullet = eT.SubElement(node, "sub_Bullet")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)
        aux_text = child
        for note in notes:
            subbullet.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", ' ', aux_text)
        subbullet.text = aux_text
        build_third_bullet(lines_sub_bullet[i], subbullet)
        i += 1
        element_not_empty = True
    return element_not_empty


def build_third_bullet(line_list, node):
    children, lines_third = find_third_bullet(line_list)
    i = 0
    element_not_empty= False
    for child in children:
        thirdbullet = eT.SubElement(node, "third_Bullet")
        aux_text = ' '.join(lines_third[i])
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', aux_text)
        for note in notes:
            thirdbullet.set('Notes' + "_" + str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", ' ', aux_text)
        thirdbullet.text = aux_text
        element_not_empty = True
        i += 1
    return element_not_empty