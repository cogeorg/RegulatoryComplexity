from dodd_Frank import get_line_list, find_title, find_subtitle,find_part, find_sec,find_paragraph, clean_note,find_bullet, find_subbullet, find_third_bullet
import re
import xml.etree.ElementTree as ET


#Funtions: build_title, build_section, build_subtitle, build_part, build_bullet, build_subbullet, build_third_bullet
#All the functions with similar structure to build_title

def build_title(line_list,node):
    """Builds the first level of the tree: Titles.
    Creates a section for each Title found in the text and
    calls the proper function to build the child nodes iteratively.

    Args:
        line_list (string list): The list of lines in the input text.
        node (object): Parent node in the tree structure.

    Returns:
        node: Object with the information of the tree level and lower levels.
        """

    children, lines_section = find_title(line_list)
    i=0                                                       # Varibale to get the element from lines_section
    for child in children:
        title = ET.SubElement(node, "Title")                  # Create the subElement Title (parent:Regulation)
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)     # Find all the notes in the Section
        aux_text=child
        for note in notes:
            title.set('Notes', clean_note(note))              # Create the "Notes" attribute
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              '', aux_text)                   # Variable name of the title without Notes
        title.text= aux_text
        build_section(lines_section[i],title)                 #Build section nodes
        build_subtitle(lines_section[i],title)                #Build subtitle nodes
        build_part(lines_section[i],title)                    #Build part nodes
        i +=1
    return node

def build_subtitle(line_list,node):
    children, lines_subtitle = find_subtitle(line_list)
    i=0
    for child in children:
        aux_text=child
        subtitle = ET.SubElement(node, "Subtitle")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            subtitle.set('Notes', clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              '', aux_text)
        subtitle.text= aux_text
        build_section(lines_subtitle[i],subtitle)                 #Build section nodes
        i +=1
    return node

def build_part(line_list,node):
    children, lines_part = find_subtitle(line_list)
    i=0
    for child in children:
        part = ET.SubElement(node, "PART")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            part.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              '', aux_text)
        part.text= aux_text
        build_section(lines_part[i],part)
        i +=1
    return node

def build_section(line_list,node):
    children, lines_section= find_sec(line_list)
    i=0
    for child in children:
        section = ET.SubElement(node, "Section")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            section.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              '', aux_text)
        section.text= aux_text
        build_paragraph(lines_section[i],section)
        i +=1
    return node


def build_paragraph(line_list,node):
    children, lines_paragraph= find_paragraph(line_list)
    i=0
    for child in children:
        paragraph = ET.SubElement(node, "Paragraph")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            paragraph.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", '', aux_text)
        paragraph.text= aux_text
        build_bullet(lines_paragraph[i],paragraph)
        i +=1
    return node

def build_bullet(line_list,node):
    children, lines_bullet= find_bullet(line_list)
    i=0
    for child in children:
        bullet = ET.SubElement(node, "Bullet")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            bullet.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", '', aux_text)
        bullet.text= aux_text
        build_subbullet(lines_bullet[i],bullet)
        i +=1
    return node

def build_subbullet(line_list,node):
    children, lines_subbullet= find_subbullet(line_list)
    i=0
    for child in children:
        subbullet = ET.SubElement(node, "subBullet")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            subbullet.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", '', aux_text)
        subbullet.text= aux_text
        build_third_bullet(lines_subbullet[i],subbullet)
        i +=1
    return node

def build_third_bullet(line_list,node):
    children, lines_third= find_third_bullet(line_list)
    i=0
    for child in children:
        thirdbullet = ET.SubElement(node, "thirdBullet")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        aux_text=child
        for note in notes:
            thirdbullet.set('Notes' +"_" +str(notes.index(note) + 1), clean_note(note))
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ", '', aux_text)
        thirdbullet.text= aux_text
        i +=1
    return node

