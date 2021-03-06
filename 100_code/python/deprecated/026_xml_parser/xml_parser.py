from lxml import etree
from xml.dom import minidom
from tree import *
from dodd_frank import get_line_list

import argparse
import xml.etree.ElementTree as eT
import os


def main(argv):
    # Get the text, line by line
    line_list = get_line_list(argv.input)
    # Set the root of the tree called Regulation
    root = etree.Element("Regulation")
    # Build the tree
    build_item(line_list, root, False, "title")

    # Build amended items
    walkAll = root.getiterator()
    for elt in walkAll:
        build_amended_item(elt)



    # Export xml
    xmlstr = minidom.parseString(eT.tostring(root)).toprettyxml(indent="   ")
    os.chdir(argv.output)

    with open("dodd_frank.xml", "w") as f:
        f.write(xmlstr)
    return True


if __name__ == "__main__":
     parser = argparse.ArgumentParser(description='Dodd-Frank xml parser .')
     parser.add_argument('-i', '--input', help='Input file name', required=True)
     parser.add_argument('-o', '--output', help='Output Directory', required=True)
     args = parser.parse_args()
     main(args)
