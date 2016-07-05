from lxml import etree
from xml.dom import minidom
import xml.etree.ElementTree as ET
from tree import build_title
from dodd_Frank import get_line_list
import sys, getopt
import os
import argparse






#Read file
def main(argv):
    file_name = args.input
    #Get the text, line by line
    line_list=get_line_list(file_name)
    #Set the root of the tree called Regulation
    root = etree.Element("Regulation")
    tree= build_title(line_list, root)

    #Export xml
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    os.chdir( args.output)
    with open("Dodd_Frank.xml", "w") as f:
        f.write(xmlstr)
    return True

if __name__ == "__main__":
    __author__ = 'Ali Limon'
    parser = argparse.ArgumentParser(description='Dodd-Frank xml parser .')
    parser.add_argument('-i','--input', help='Input file name',required=True)
    parser.add_argument('-o','--output',help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)