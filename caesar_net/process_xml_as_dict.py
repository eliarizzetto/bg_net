import xmltodict as xd


caes_gal_path = 'caes-gal.xml'
cic_att_path = 'cic-att.xml'

with open(caes_gal_path, 'r', encoding='utf-8') as f:
    data_xml = f.read()
    data_dict = xd.parse(data_xml)

    for x in data_dict['proiel']['source']['div']:
        pass