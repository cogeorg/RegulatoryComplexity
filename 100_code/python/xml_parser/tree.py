from dodd_Frank import get_line_list, find_title, find_subtitle,find_part, find_sec,find_paragraph
#find_bullet, find_subbullet
import re
import xml.etree.ElementTree as ET


#Funtions: build_title, build_section, build_subtitle, build_part
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
    i=0                                                      # Varibale to get the element from lines_section
    for child in children:
        title = ET.SubElement(node, "Title")                  # Create the subElement Title (parent:Regulation)
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt', child)     # Find all the notes in the Section
        for note in notes:
            title.set('Notes',re.sub(";NOTE", '', note))      # Create the "Notes" attribute
            aux_text = re.sub(" &lt;&lt" + note + "&gt;&gt; ",
                              '', child)                      # Variable name of the title without Notes
        if aux_text == "": aux_text=child
        title.set('id',                                       #Create the "Id" attribute, with the name of the title
                  re.findall(r"TITLE\s*[V,I,X]+[--]*[,\sA-Z]*",aux_text)[0])
        build_section(lines_section[i],title)                 #Build section nodes
        build_subtitle(lines_section[i],title)                #Build subtitle nodes
        build_part(lines_section[i],title)                    #Build part nodes
        i +=1
        aux_text=""
    return node

def build_subtitle(line_list,node):
    children, lines_title = find_subtitle(line_list)
    i=0
    for child in children:
        subtitle = ET.SubElement(node, "Subtitle")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        if len(notes)>0:
            subtitle.set('Notes',re.sub(";NOTE", '', notes[0]))
            subtitle.text= re.sub("&lt;&lt"+notes[0]+"&gt;&gt;", '', child)
        else:
            subtitle.text=child
        build_section(lines_title[i],subtitle)
        i +=1
    return node

def build_part(line_list,node):
    children, lines_title = find_subtitle(line_list)
    i=0
    for child in children:
        part = ET.SubElement(node, "PART")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        if len(notes)>0:
            part.set('Notes',re.sub(";NOTE", '', notes[0]))
            part.text=  re.sub("&lt;&lt"+notes[0]+"&gt;&gt;", '', child)
        else:
            part.text=child
        build_section(lines_title[i],part)
        i +=1
    return node

def build_section(line_list,node):
    children, lines_title= find_sec(line_list)
    i=0
    for child in children:
        section = ET.SubElement(node, "Section")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        if len(notes)>0:
            section.set('Notes',re.sub(";NOTE", ' ', notes[0]))
            section.text= re.sub("&lt;&lt"+notes[0]+"&gt;&gt;", ' ', child)
        else:
            section.text=child
        build_paragraph(lines_title[i],section)
        i +=1
    return node


def build_paragraph(line_list,node):
    children, lines_title= find_paragraph(line_list)
    i=0
    for child in children:
        paragraph = ET.SubElement(node, "Paragraph")
        notes = re.findall(r'&lt;&lt(.*?)&gt;&gt',child)
        if len(notes)>0:
            paragraph.set('Notes',re.sub(";NOTE", ' ', notes[0]))
            paragraph.text= re.sub("&lt;&lt"+notes[0]+"&gt;&gt;", ' ', child)
        else:
            paragraph.text=child
        #build_bullet(lines_title[i],paragraph)
        i +=1
    return node





