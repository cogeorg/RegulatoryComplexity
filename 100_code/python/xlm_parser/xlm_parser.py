from lxml import etree
from xml.dom import minidom
import xml.etree.ElementTree as ET

from tree import build_title
from dodd_Frank import get_line_list

#Read file
file_name = "RegulatoryComplexity/001_raw_data/htm/DODDFRANK.htm"
#Get the text, line by line
line_list=get_line_list(file_name)
#Set the root of the tree called Regulation
root = etree.Element("Regulation")
tree= build_title(line_list, root)

#Export xml
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open("010_cleaned_data/Dodd_Frank.xml", "w") as f:
    f.write(xmlstr)
