import re
import os
import argparse


def main(argv):

    with open (argv.input, "r") as myfile:
        data = myfile.read()

    data = re.sub('<?xml version="1.0" ?>','',data)
    data = re.sub('Regulation>','body>',data)

    tag_names = ['Title','Subtitle','Part','Section', 'Paragraph', 'Bullet', 'sub_Bullet', 'third_Bullet']
    tag_class=['class="ex1"', 'class="ex2"', 'class="ex3"', 'class="ex4"',
               'class="ex5"', 'class="ex6"', 'class="ex7"','class="ex8"' ]


    for tag in tag_names:
        # divisions
        data = re.sub('<' + tag_names[tag_names.index(tag)]
                      ,'<div ' + tag_class[tag_names.index(tag)],data)

        #classes
        data = re.sub('</' + tag_names[tag_names.index(tag)]
                      ,'</div',data)


    head= """<!DOCTYPE html> <html>
    <head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css">
    </head>"""

    tail= """
    </html>
    """

    data = head + data + tail

    os.chdir(argv.output)
    filename = 'dodd_frank.html'
    f = open(filename,'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)


