import re
import argparse


def get_list_legal(reg1, reg2, reg3, data_xml, legal_references):
    for reg in reg1:
        for aux in reg2:
            for type in reg3:
                mylist = re.findall(reg + aux + type  , data_xml)       # Find all with the concatenated regex
                mylist = list(set(mylist))                              # Unique elements.
                legal_references = legal_references + mylist            # Add mylist (new) to legal_references (old)
    return legal_references


def create_ref_type():
    ref_type = []
    ref_type.append(r'')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\)')
    ref_type.append(r'\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\([0-9]\)\([A-Z]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\([0-9]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([a-z]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\([1-9]\)\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{2}]+[a-z]\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\-[0-9]\)')
    ref_type.append(r'\s\([0-9{1}]\s[U\.S\.C]+\s[0-9{1}]\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\-[0-9]\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([0-9]\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\([a-z]\)\([0-9]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\s' + re.escape(r'et seq.)'))
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([a-z]\)\([0-9]\)\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]\)')
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\-\s*[0-9]+\([a-z]+\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\-\s*[0-9]+\)')
    ref_type.append(r'\s[U\.S\.C]+\s[Ap\.]+\)')
    return ref_type



def main(argv):
    argv.input
    with open (argv.input, "r") as myfile:
        data_xml = myfile.read()

    legal_references = []


    # Find Title references.
    # For instance: title 1
    regex = []
    regex.append(r'title')
    ref_aux = []
    ref_aux.append(r'\s[0-9]+')
    ref_type = create_ref_type()                    # create_ref_type is a list of regex
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)  # Find all for concatenated
                                                                                             # regex

    # Find Subtitle references.
    # For instance: subtitle A
    regex = []
    regex.append(r'subtitle')
    ref_aux = []
    ref_aux.append(r'\s[A-Z]+')
    ref_type = create_ref_type()
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)


    # Find Section references.
    # For instance: substitles (c) through (g)
    regex = []
    regex.append(r'subtitles')
    ref_aux = []
    ref_aux.append(r'\s[A-Z]+\s[and]+\s[A-Z]+')
    ref_aux.append(r'\s[A-Z]+\s[through]+\s[A-Z]+')
    ref_type.append(r'')                                # For these types of regex and ref_aux, ref_type is null
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)


    # Find Section references.
    # For instance: section 7701(a)(36)
    regex = []
    regex.append(r'section')
    ref_aux = []
    ref_aux.append(r'\s[0-9]+')
    ref_aux.append(r'\s[0-9]+\([a-z]+\)')
    ref_aux.append(r'\s\([0-9]+\)\s[or]+\s\([0-9]+\)')
    ref_aux.append(r'\s[0-9]+\([a-z]+\)\([0-9]+\)')
    ref_aux.append(r'\s[0-9]+\([a-z]+\)\([0-9]+\)\([A-B]+\)')
    ref_type = create_ref_type()                      # create_ref_type is a list of regex
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # Find Section references.
    # For instance: subsection (c)
    regex = []
    regex.append(r'subsection')
    ref_aux = []
    ref_aux.append(r'\s\([a-z]+\)')
    ref_aux.append(r'\s\([a-z]+\)\s[or]+\s\([a-z]+\)')
    ref_aux.append(r'\s\([a-z]+\)\([0-9]+\)')
    ref_type = create_ref_type()
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # Find Section references.
    # For instance: subsections (c) through (g)
    regex = []
    regex.append(r'subsections')
    ref_aux = []
    ref_aux.append(r'\s\([a-z]+\)\s[and]+\s\([a-z]+\)')
    ref_aux.append(r'\s\([a-z]+\)\s[through]+\s\([a-z]+\)')
    ref_aux.append(r'\s\([a-z]+\)[\(0-9\)]*\,\s\([a-z]+\)[\(0-9\)]*\,\s\([a-z]+\)[\(0-9\)]*\,\s[and]+\s\([a-z]+\)[\(0-9\)]*')
    ref_type = create_ref_type()
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # Find paragraph references.
    # For instance: paragraph (1)
    regex = []
    regex.append(r'paragraph')
    ref_aux = []
    ref_aux.append(r'\s\([0-9]+\)')
    ref_aux.append(r'\s\([0-9]+\)\s[or]+\s\([0-9]+\)')
    ref_aux.append(r'\s\([0-9]+\)\([A-B]+\)')
    ref_type = create_ref_type()
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance: paragraphs (1) and (2)
    regex = []
    regex.append(r'paragraphs')
    ref_aux = []
    ref_aux.append(r'\s\([0-9]+\)\s[and]+\s\([0-9]+\)')
    ref_aux.append(r'\s\([0-9]+\)\s[through]+\s\([0-9]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)


    # Find subparagraph references.
    # For instance:subparagraph (A)
    regex = []
    regex.append(r'subparagraph')
    ref_aux = []
    ref_aux.append(r'\s\([A-Z]+\)')
    ref_aux.append(r'\s\([A-Z]+\)\s[or]+\s\([A-Z]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance:subparagraphs (A) and (B)
    regex = []
    regex.append(r'subparagraphs')
    ref_aux = []
    ref_aux.append(r'\s\([A-Z]+\)\s[and]+\s\([A-Z]+\)')
    ref_aux.append(r'\s\([A-Z]+\)\s[through]+\s\([A-Z]+\)')
    ref_aux.append(r'\s\([A-Z]+\)\,\s\([A-Z]+\)\,\s\([A-Z]+\)\,\s[and]+\s\([A-Z]+\)')
    ref_aux.append(r'\s\([A-Z]+\)\,\s\([A-Z]+\)\,\s[and]+\s\([A-Z]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # Find clause references.
    # For instance:clause (i)
    regex = []
    regex.append(r'clause')
    ref_aux = []
    ref_aux.append(r'\s\([ivx]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance:clauses (i) and (ii)
    regex = []
    regex.append(r'clauses')
    ref_aux = []
    ref_aux.append(r'\s\([ivx]+\)\s[and]+\s\([ivx]+\)')
    ref_aux.append(r'\s\([ivx]+\)\s[through]+\s\([ivx]+\)')
    ref_aux.append(r'\s\([ivx]+\)\,\s\([ivx]+\)\,\s\([ivx]+\)\,\s[and]+\s\([ivx]+\)')
    ref_aux.append(r'\s\([ivx]+\)\,\s\([ivx]+\)\,\s[and]+\s\([ivx]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # Find subclause references.
    # For instance:subclause (I)
    regex = []
    regex.append(r'subclause')
    ref_aux = []
    ref_aux.append(r'\s\([IVX]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance:subclause (I) and (II)
    regex = []
    regex.append(r'subclauses')
    ref_aux = []
    ref_aux.append(r'\s\([IVX]+\)\s[and]+\s\([IVX]+\)')
    ref_aux.append(r'\s\([IVX]+\)\s[through]+\s\([IVX]+\)')
    ref_aux.append(r'\s\([IVX]+\)\,\s\([ivx]+\)\,\s\([IVX]+\)\,\s[and]+\s\([IVX]+\)')
    ref_aux.append(r'\s\([IVX]+\)\,\s\([ivx]+\)\,\s[and]+\s\([IVX]+\)')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    #Find  SEC , PART, Subtitle and TITLE
    # For instance: SEC. 100
    regex = []
    regex.append(r'SEC.')
    ref_aux = []
    ref_aux.append(r'\s[0-9]+')
    ref_type = []
    ref_type.append(r'')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance: PART I
    regex = []
    regex.append(r'PART')
    ref_aux = []
    ref_aux.append(r'\s[IVX]+')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance: Subtitle II
    regex = []
    regex.append(r'Subtitle')
    ref_aux = []
    ref_aux.append(r'\s[A-Z]+')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)

    # For instance: TITLE I
    regex = []
    regex.append(r'TITLE')
    ref_aux = []
    ref_aux.append(r'\s[IVX]+')
    legal_references = get_list_legal(regex, ref_aux, ref_type, data_xml, legal_references)



    # Simple legal_references for auto-reference
    legal_references.append("this section")
    legal_references.append("this subsection")
    legal_references.append("this paragraph")
    legal_references.append("this subtitle")
    legal_references.append("this Act")
    legal_references.append("this title")





    legal_references= list(set(legal_references))

     #Sort and export
    legal_references = sorted(legal_references)
    file = open(argv.output + "legal_references_extra.txt", 'w')
    for item in legal_references:
        file.write("%s\n"%item)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
