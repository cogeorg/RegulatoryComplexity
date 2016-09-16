import re
import argparse



def main(argv):
    argv.input
    with open (argv.input, "r") as myfile:
        data_xml = myfile.read()

    # Regex first part of the Legal reference
    # For instance: The Farm Credit, The Federal Advisory Comitee, The Clayton
    regex = []
    regex.append(r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+\-[A-Z]{1}[a-z]+')
    regex.append(r'[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+')
    regex.append(r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[and]+\s[A-Z]{1}[a-z]+')
    regex.append( r'the\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[and]+\s[A-Z]{1}[a-z]+')
    regex.append(r'[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+\s[and]+\s[A-Z]{1}[a-z]+')


    # Regex second part of the Legal Reference
    ref_aux = []
    ref_aux.append(r' Act')
    ref_aux.append(r' Act of')
    ref_aux.append(r' Act Amendments')

    # Regex thrid part of the legal reference, which representes the year of the act and
    # the specifict part.
    # For instance: 1956 (12 U.S.C 19), (15 U.S.C 1843(j)(2)), (12 U.S.C 3201 et seq.)
    ref_type = []
    ref_type.append(r'\s[0-9{4}]+')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\([0-9]\)\([A-Z]\)\)')
    ref_type.append( r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\([0-9]\)\)')
    ref_type.append( r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\([a-z]\)\)')
    ref_type.append( r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([a-z]\)\)')
    ref_type.append( r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\([1-9]\)\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{2}]+[a-z]\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\-[0-9]\)')
    ref_type.append(r'\s\([0-9{1}]\s[U\.S\.C]+\s[0-9{1}]\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\-[0-9]\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([0-9]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+\([a-z]\)\([0-9]\)\)')
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9{4}]+\s' + re.escape(r'et seq.)'))
    ref_type.append( r'\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]\([a-z]\)\([0-9]\)\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]\)')
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\-\s*[0-9]+\([a-z]+\)\)')
    ref_type.append( r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\s' + re.escape(r'et seq.)'))
    ref_type.append(r'\s[0-9{4}]+\s\([0-9{2}]+\s[U\.S\.C]+\s[0-9]+[a-z]+\-\s*[0-9]+\)')
    ref_type.append(r'\s\([0-9]+\s[U\.S\.C]+\s[Ap\.]+\)')


    legal_references = []


    # Iterate over all the possible regexs.
    for reg in regex:
        for aux in ref_aux:
            flag = True
            for type in ref_type:
                # Legal references can/cannot be followed by third part regex.
                # For instance: the Federal Home Loan Bank Act.
                if flag and aux == ref_aux[0]:
                   mylist = re.findall(reg + aux, data_xml)
                   #Make a list of unique elements 
                   mylist = list(set(mylist))
                   legal_references = legal_references + mylist
                   flag = False
                # All the other references
                # For instance: the Federal Home Loan Bank Act .
                mylist = re.findall(reg + aux + type , data_xml)
                mylist = list(set(mylist))
                legal_references = legal_references + mylist

    #Sort and export
    legal_references = sorted(legal_references)
    file = open(argv.output + "legal_references.txt", 'w')
    for item in legal_references:
        file.write("%s\n"%item)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
