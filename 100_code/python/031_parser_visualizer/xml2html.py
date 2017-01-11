import re
import lxml.etree as etree
from io import StringIO, BytesIO
import glob
import argparse

def main(argv):
    #parse XML
    parse = etree.parse(argv.input)
    # make a stream out of it
    html = ""
    elTail = ""
    c = 0
    dfa = {}
    for action, elem in etree.iterwalk(parse, events=('start', 'end')):
        #print action, "|", elem.tag, "|", elem.text, "|", elem.tail
        if action == "start":
            if elem.tag == "title":
                if c == 0:
                    html = ' '.join(html.split())
                    head = """<!DOCTYPE html><html><head></head><body><div class = "ex1">TITLE 0."""
                    tail = """</div></body></html>"""
                    title = head + html + tail
                    name = "title_" + str(c) + ".html"
                    dfa[name] = title
                    c += 1
                    html = ""
                    html += '<div class = "ex1">' + 'TITLE '
                else:
                    html = ' '.join(html.split())
                    head = """<!DOCTYPE html><html><head></head><body>"""
                    tail = """</body></html>"""
                    title = head + html + tail
                    name = "title_" + str(c) + ".html"
                    dfa[name] = title
                    c += 1
                    html = ""
                    html += '<div class = "ex1">' + 'TITLE '
            elif elem.tag == "subtitle":
                html += '<div class = "ex2">' + 'SUBTITLE '
            elif elem.tag == "part":
                html += '<div class = "ex3">' + 'PART '
            elif elem.tag == "section":
                html += '<div class = "ex4">' + 'SEC. '
            elif elem.tag == "subsection":
                html += '<div class = "ex5">'
            elif elem.tag == "paragraph":
                html += '<div class = "ex6">'
            elif elem.tag == "subparagraph":
                html += '<div class = "ex7">'
            elif elem.tag == "clause":
                html += '<div class = "ex8">'
            elif elem.tag == "subclause":
                html += '<div class = "ex9">'
            elif elem.tag == "item":
                html += '<div class = "ex10">'
            elif elem.tag == "subitem":
                html += '<div class = "ex11">'
            elif elem.tag == "quoted-block":
                html += '<div class = "amended">'
            elif elem.tag == "after-quoted-block":
                html += '</div>'
                if elem.text != None:
                    html += elem.text.strip() + ' '
            elif (elem.tag == "enum") or (elem.tag == "continuation-text") or (elem.tag == "quoted-block-continuation-text"):
                if elem.text != None:
                    html += elem.text.strip() + ' '
            elif elem.tag == "text":
                try:
                    if elem.attrib['display-inline'] == "no-display-inline":
                        if elem.text != None:
                            html += '<div class = "singlepar">' + elem.text.strip() + ' '
                    else:
                         if elem.text != None:
                             html += elem.text.strip() + ' '
                except:
                    if elem.text != None:
                        html += elem.text.strip() + ' '
            elif elem.tag == "header":
                if elem.text != None:
                    html += elem.text.strip() + '.-- '
            elif elem.tag == "term":
                if elem.text != None:
                    html += '"' + elem.text.strip() + '" '
                    if elem.tail != None:
                        html += elem.tail.strip() + ' '
            elif (elem.tag == "quote") and (elem.getparent().tag != "toc-entry") and (elem.getparent().tag != "official-title"):
                if elem.text != None:
                    html += '"' + elem.text.strip() + '" '
                    if elem.tail != None:
                        html += elem.tail.strip() + ' '
                else:
                    if elem.tail != None:
                        html += '"'
                        elTail = elem.tail.strip() + ' '
            elif elem.tag == "header-in-text":
                if elem.text != None:
                    html += elem.text.strip()
                if elem.tail != None:
                    html += elem.tail.strip() + ' '
            elif (elem.tag == "enum-in-header") or (elem.tag == "italic") or (elem.tag == "fraction") or (elem.tag == "list") or (elem.tag == "list-item") or (elem.tag == "act-name"):
                if elem.text != None:
                    html += elem.text.strip() + ' '
                if elem.tail != None:
                    html += elem.tail.strip() + ' '
            elif (elem.tag == "short-title"):
                if elem.text != None:
                    html += elem.text.strip()
                if elem.tail != None:
                    html += elem.tail.strip() + ' '
            else:
                continue

        if action == "end":
            if (elem.tag == "title") or (elem.tag == "subtitle") or (elem.tag == "part") or (elem.tag == "section") or (elem.tag == "subsection") or (elem.tag == "paragraph") or (elem.tag == "subparagraph") or (elem.tag == "clause") or (elem.tag == "subclause") or (elem.tag == "item") or (elem.tag == "subitem"):
                html += '</div>'
            elif elem.tag == "quote":
                if elem.text == None:
                    html += '" ' + elTail
                    elTail = ""
            else:
                continue

    # include correct tags for paragraphs starting without numbering
    for name, title in dfa.items():
        print name
        parts = title.split("<")
        update = []
        bullet = 0
        amended = 0
        amBullet = 0
        for part in parts:
            if part != "":
                # first, delete unnecessary whitespace
                part = re.sub(r'(")\s([^a-z])', r'\1\2', part)
                #then include tags for paragraphs
                if part.startswith('div class = "singlepar"'):
                    newPart = part.replace("singlepar", "ex5")
                    update.append("<" + newPart)
                    if amended == 0:
                        bullet = 1
                    else:
                        amBullet = 1
                elif part.startswith('div class = "amended">'):
                    update.append("<" + part)
                    amended = 1
                elif (part.startswith('/div>')) and (len(part)>5):
                    update.append("<" + part)
                    amended = 0
                else:
                    if (bullet == 0) and (amBullet == 0):
                        update.append("<" + part)
                    elif (bullet == 1) and (amBullet == 0):
                        if (part.startswith('div class = "ex2"')) or (part.startswith('div class = "ex3"')) or (part.startswith('div class = "ex4"')) or (part.startswith('/body')):
                            if amended == 0:
                                update.append('</div>')
                                update.append("<" + part)
                                bullet = 0
                            else:
                                update.append("<" + part)
                        else:
                            update.append("<" + part)
                    else:
                        if (part.startswith('div class = "ex2"')) or (part.startswith('div class = "ex3"')) or (part.startswith('div class = "ex4"')) or ((part.startswith('/div')) and (len(part) > 4)):
                            update.append('</div>')
                            update.append("<" + part)
                            amBullet = 0

        # words version:
        if argv.type == "words":
            # include preclassification
            htmlString = ""
            for item in update:
                htmlString += item
            if argv.words:
                operands_operators = read_txt_files(argv.words)
                for type, operand, length in operands_operators:
                    my_regex =  r"\s[\-\,\(\"]*" + re.escape(operand) + r"[s\-\.\,\`\'\;\:\)\"]*[\s]"
                    mylist = re.findall(my_regex, htmlString, flags=re.IGNORECASE)
                    mylist = list(set(mylist))
                    for word in mylist:
                        replacement = ' <span class="' + type + '">' + word.replace(" ", "__") + '</span> '
                        htmlString = htmlString.replace(word, replacement)
                htmlString = htmlString.replace("__", " ")

            parts = []
            split1 = htmlString.split('<div')
            for s in split1:
                if s == split1[0]:
                    parts.append(s)
                else:
                    parts.append('<div' + s)
            update = []
            for p in parts:
                split2 = p.split('</div')
                for t in split2:
                    if t == split2[0]:
                        update.append(t)
                    else:
                        update.append('</div' + t)


            # save file
            with open(argv.output + name, "w") as g:
                amended = 0
                for item in update:
                    item = re.sub('--', '', item)
                    if amended == 0:
                        if item == '<div class = "amended">':
                            amended = 1
                        else:
                            g.write(item + "\n")
                    else:
                        if (item.startswith('</div>')) and (len(item) > 6):
                            item = item.replace('</div>', '"')
                            g.write(item + "\n")
                            amended += -1
                        elif item == '</div>':
                            g.write(item + "\n")
                        else:
                            item = re.sub(r'(<div class = "ex.+?">)', r'\1"', item)
                            g.write(item + "\n")

        elif argv.type == "coherence":
            # include preclassification
            htmlString = ""
            for item in update:
                htmlString += item
            if argv.words:
                operands_operators = read_txt_files_coherence(argv.words)
                for type, operand, length in operands_operators:
                    my_regex =  r"\s[\-\,\(\"]*" + re.escape(operand) + r"[s\-\.\,\`\'\;\:\)\"]*[\s]"
                    mylist = re.findall(my_regex, htmlString, flags=re.IGNORECASE)
                    mylist = list(set(mylist))
                    for word in mylist:
                        replacement = ' <span class="' + type + '">' + word.replace(" ", "__") + '</span> '
                        htmlString = htmlString.replace(word, replacement)
                htmlString = htmlString.replace("__", " ")

            parts = []
            split1 = htmlString.split('<div')
            for s in split1:
                if s == split1[0]:
                    parts.append(s)
                else:
                    parts.append('<div' + s)
            update = []
            for p in parts:
                split2 = p.split('</div')
                for t in split2:
                    if t == split2[0]:
                        update.append(t)
                    else:
                        update.append('</div' + t)


            # save file
            with open(argv.output + name, "w") as g:
                amended = 0
                for item in update:
                    item = re.sub('--', '', item)
                    if amended == 0:
                        if item == '<div class = "amended">':
                            amended = 1
                        else:
                            g.write(item + "\n")
                    else:
                        if (item.startswith('</div>')) and (len(item) > 6):
                            item = item.replace('</div>', '"')
                            g.write(item + "\n")
                            amended += -1
                        elif item == '</div>':
                            g.write(item + "\n")
                        else:
                            item = re.sub(r'(<div class = "ex.+?">)', r'\1"', item)
                            g.write(item + "\n")


        # sentence-parts version:
        else:
            # create headlines
            bullets = 0
            amended = 0
            with open(argv.output + name, "w") as g:
                for item in update:
                    if amended == 0:
                        if item.startswith('<div class = "ex5">'):
                            item = re.sub(r'(\(.+?\)\s)([A-Z].*?\.)(--)', r'\1<span class = "H">\2</span>', item)
                            g.write(item + "\n")
                        elif (item.startswith('<div class = "ex6">')) or (item.startswith('<div class = "ex7">')) or (item.startswith('<div class = "ex8">')) or (item.startswith('<div class = "ex9">')) or (item.startswith('<div class = "ex10">')) or (item.startswith('<div class = "ex11">')):
                            item = re.sub(r'(\(.+?\)\s)([A-Z].*?\.)(--)', r'<br />\1<span class = "H">\2</span>', item)
                            item = re.sub(r'<div class = "ex.+?">', '', item)
                            bullets += 1
                            g.write(item + "\n")
                        elif item =='</div>':
                            if bullets > 0:
                                bullets += -1
                            else:
                                g.write(item + "\n")
                        elif item =='<div class = "amended">':
                            amended += 1
                        else:
                            item = re.sub('--', '', item)
                            g.write(item + "\n")
                    else:
                        if item.startswith(r'<div class'):
                            item = re.sub(r'<div class = "ex.+?">', '', item)
                            bullets += 1
                            item = re.sub(r'(\(.+?\)\s)([A-Z].*?\.)(--)', r'<br />"\1<span class = "H">\2</span>', item)
                            if (item.startswith('SEC')):
                                item = '<br />' + '"' + item
                                item = re.sub('--', '', item)
                            g.write(item + "\n")
                        elif item =='</div>':
                            if bullets > 0:
                                bullets += -1
                            else:
                                g.write(item + "\n")
                        elif (item.startswith('</div>')) and (len(item) > 6):
                            item = item.replace('</div>', '"')
                            g.write(item + "\n")
                            amended += -1
                        else:
                            item = re.sub('--', '', item)
                            g.write('"' + item + "\n")


def read_txt_files(file):
    list_tuples = []
    for filename in glob.glob(file + '/*.txt'):
        key = filename.split("/")
        key = key[-1].replace(".txt","")
        key = key.replace("_extra", "")
        key = key.replace("_special", "")
        f = open(filename, 'r')
        for element in f.readlines():
            aux_text = element.strip('\n')
            aux_text = aux_text.strip('\r')
            aux_text = aux_text.strip()
            tuple = (key , aux_text, len(aux_text.split(" ")))
            list_tuples.append(tuple)
    return sorted(list_tuples, key=lambda x: x[2],reverse=True)

def read_txt_files_coherence(file):
    list_tuples = []
    for f in []:
        filename = file + f
        key = f[0]
        f = open(filename, 'r')
        for element in f.readlines():
            aux_text = element.strip('\n')
            aux_text = aux_text.strip('\r')
            aux_text = aux_text.strip()
            tuple = (key , aux_text, len(aux_text.split(" ")))
            list_tuples.append(tuple)
    return sorted(list_tuples, key=lambda x: x[2],reverse=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-t', '--type', help='Type (Words or Sentence-Parts)', required=True)
    parser.add_argument('-w', '--words', help='Classified words', required=False)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
