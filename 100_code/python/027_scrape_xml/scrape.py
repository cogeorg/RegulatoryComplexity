import requests
from xml.etree import ElementTree

response = requests.get('https://www.congress.gov/111/bills/hr4173/BILLS-111hr4173enr.xml')

xml = response.content

with open('DFA.xml','w') as f:
    f.write(xml)
