import re
import glob
import os
import argparse


def main(argv):
    
    # get working directory
    os.chdir(argv.input)

    for file in glob.glob("*.html"):

        # filename replacements
        titles = ["TITLE I-", "TITLE II-", "TITLE III-", "TITLE IV-", "TITLE V-", 
                    "TITLE VI-", "TITLE VII-", "TITLE VIII-", "TITLE IX-", "TITLE X-",
                    "TITLE XI-", "TITLE XII-", "TITLE XIII-", "TITLE XIV-", "TITLE XV-",
                    "TITLE XVI-"]
        newTitles = ["title_1", "title_2", "title_3", "title_4", "title_5", "title_6", 
                        "title_7", "title_8", "title_9", "title_10", "title_11", 
                        "title_12", "title_13", "title_14", "title_15", "title_16"]

        # get current file name
        base = os.path.basename(file)

        # replace file name
        for title in titles:
            if base.startswith(title):
                base = newTitles[titles.index(title)] + ".html"
            else: continue

        with open (file, "r") as myfile:
            data = myfile.read()

        # find headlines
        replacement = re.findall("\)\s([A-Z].{1,110}?\.--)", data)
        # only store unique headlines
        uniqueReplacement = []
        for line in replacement:
            if line not in uniqueReplacement:
                uniqueReplacement.append(line)

        # sort headlines by length
        replacement = uniqueReplacement
        replacement.sort(key = len, reverse = True)

        # include spans for headlines
        for line in replacement:
            data = re.sub(line, "<span class=H>" + line +"</span>", data)

        # include <br /> tags
        data = re.sub(r"(\s)(\(.{1,3}\)\s<span class=H>)", r" <br />\2", data)
        data = re.sub(r"(\s)(``\(.{1,3}\)\s<span class=H>)", r" <br />\2", data)

        #delete "--" in front of enumerations
        data = re.sub("([a-z]|\)|'')(--)", r'\1', data)

        # delete "\" around numbers
        data = re.sub(r"\\", "", data)

        f = open(argv.output + base,'w')
        f.write(data)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank sub-headlines.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
