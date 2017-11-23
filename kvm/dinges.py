import xml.etree.ElementTree as ET

tree = ET.parse('kvmtrois.xml')
doc = tree.getroot()

change = doc.find('devices')

tree.write('kvmtrois.xml')
print(change)