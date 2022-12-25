import xml.etree.ElementTree as ET

caes_gal_path = 'caes-gal.xml'
cic_att_path = 'cic-att.xml'

tree = ET.parse(caes_gal_path)

root = tree.getroot()


sentences = root.find('div')

for s in sentences:
    print(s)