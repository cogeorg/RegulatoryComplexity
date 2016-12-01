import re

# open Dodd-Frank XML file
with open("dodd_frank.xml") as f:
	data = f.read()

# get rid of structure
data = data.replace("\n", " ")

# find all quoted terms after the word "term"
defs = re.findall("\sterm\s(.*?)'[\s|'|,|;|-]", data)
cleanDefs = []
for item in defs:
	if item.startswith("`"):
		item = item.strip("`")
		item = item.strip()
		if item not in cleanDefs:
			cleanDefs.append(item)

# find all quoted terms after the word "terms"
addDefs = re.findall("\sterms\s(.*?)<", data)
for item in addDefs:
	if item.startswith("`"):
		terms = re.findall("`(.*?)'", item)
		for term in terms:
			term = term.strip("`")
			term = term.strip()
			if term not in cleanDefs:
				cleanDefs.append(term)

# sort definitions
cleanDefs.sort()

#save in txt file
with open("EconomicOperands_special.txt", 'w') as f:
	for item in cleanDefs:
		f.write(item)
		f.write("\n")
