import requests
from xml.etree import ElementTree

response = requests.get('https://www.congress.gov/111/bills/hr4173/BILLS-111hr4173pp.xml')

xml = response.content

udata=xml.decode("utf-8")
asciidata=udata.encode("ascii","ignore")

with open('/home/sabine/Dokumente/Git/RegulatoryComplexity/001_raw_data/xml/DFA_pp.xml','w') as f:
    f.write(asciidata)
