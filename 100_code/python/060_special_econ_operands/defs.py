import re
import lxml.etree as etree
import argparse
import glob

def main(argv):
	definitions = []
	# open titles
	for file in glob.glob(argv.input + "*.html"):
		with open(file) as f:
			data = f.read()

		# get rid of structure
		data = data.replace("\n", " ")

		# find all quoted terms after the word "term"
		defs = re.findall('\sterm\s"(.*?)"', data)
		for term in defs:
			if term not in definitions:
				definitions.append(term)

		# find all quoted terms after the word "terms"
		addDefs = re.findall("\sterms\s(.*?)<", data)
		for item in addDefs:
			if item.startswith('"'):
				terms = re.findall('"(.*?)"', item)
				for term in terms:
					term = term.strip()
					if term not in definitions:
						definitions.append(term)

	# sort definitions
	definitions.sort(key=len)
	definitions = definitions[::-1]

	#save in txt file
	with open(argv.output + "EconomicOperands_special.txt", 'w') as f:
		for item in definitions:
			f.write(item)
			f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract terms.')
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', required=True)
    args = parser.parse_args()
    main(args)
