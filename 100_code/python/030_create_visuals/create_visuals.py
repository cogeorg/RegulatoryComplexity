import re
import csv
import glob
import unicodedata
import argparse




def main(argv):

    with open (argv.input, "r") as myfile:
        data_xml = myfile.read()

    data_xml = data_xml.replace('<?xml version="1.0" ?>', '')
    data_xml = data_xml.replace('Regulation>', 'body>')

    #delete notes
    my_regex = r" Notes(.*?)>"
    data_xml = re.sub(my_regex, ">", data_xml)
    data_xml = data_xml.strip("\n")


    tag_names = ['title','subtitle','part','section', 'paragraph',
                 'bullet', 'two_bullet', 'three_bullet', 'four_bullet', 'five_bullet', 'six_bullet']
    tag_class=['class="ex1"', 'class="ex2"', 'class="ex3"', 'class="ex4"',
               'class="ex5"', 'class="ex6"', 'class="ex7"','class="ex8"',
               'class="ex9"','class="ex10"','class="ex11"']

    data_xml = format_text(data_xml)
    data_title = re.findall(r'<title>(.*?)</title>', data_xml)
    title_names = re.findall(r'<title>(.*?)<', data_xml)
    operands_operators = read_txt_files(argv.words)
    i = 0
    for data in data_title:
        for tag in tag_names:
            # divisions
            data = re.sub('<' + tag_names[tag_names.index(tag)]
                          ,' <div ' + tag_class[tag_names.index(tag)],data)

            #classes
            data = re.sub('</' + tag_names[tag_names.index(tag)]
                          ,' </div',data)

        # Attributes, EconomicOperands, GrammaticalOperators, LegalOperators, LegalReferences
        # LogicalOperators, Other, RegulationOperators
        for type, operand, length in operands_operators:
            my_regex =  r"\s[\-\,]*" + re.escape(operand) + r"[s\-\.\,\`\'\;\:\)]*[\s]"
            mylist = re.findall(my_regex, data, flags=re.IGNORECASE)
            mylist = list(set(mylist))
            for word in mylist:
                replacement = ' <span class="' + type[0] + '"> ' + word.replace(" ", "__") + ' </span> '
                data = data.replace(word, replacement)

        data = data.replace("__", " ")

        head= """<!DOCTYPE html> <html>
        <head>
        </head>"""

        tail= """
        </html>
        """

        data = head + data + tail

        filename = title_names[i].strip() + ".html"
        f = open(argv.output + filename,'w')
        f.write(data)
        f.close()
        i +=1



def read_txt_files(file):
    list_tuples = []
    for filename in glob.glob(file + '/*.txt'):
        key = filename.split("/")
        key = key[-1].replace(".txt","")
        key = key.replace("LegalReferences_inside", "LegalReferences")
        f = open(filename, 'r')
        for element in f.readlines():
            aux_text = element.strip('\n')
            aux_text = aux_text.strip('\r')
            aux_text = aux_text.strip()
            tuple = (key , aux_text, len(aux_text.split(" ")))
            list_tuples.append(tuple)
    return sorted(list_tuples, key=lambda x: x[2],reverse=True)


def format_text(data):
    data = data.replace('  ', '')
    data = data.replace('\n',' ')
    data = data.replace('.--','.-- ')
    return data



        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-w', '--words', help='Classified words', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)

