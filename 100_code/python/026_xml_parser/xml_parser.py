from lxml import etree
from xml.dom import minidom
from tree import build_title
from dodd_frank import get_line_list

import argparse
import xml.etree.ElementTree as eT
import os

def main(argv):
    file_name = argv.input
    # Get the text, line by line
    line_list = get_line_list(file_name)
    # Set the root of the tree called Regulation
    root = etree.Element("Regulation")
    build_title(line_list, root)

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
