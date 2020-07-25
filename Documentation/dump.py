"""Creates a source dump HTML file"""

from xml.etree import ElementTree as ET
from .generator import Generator

class Dump(Generator):
    def __init__(self, titletext, config, **kwargs):
        super().__init__(titletext, **kwargs)
        self.number_of_data_lists = len(config.data_list)
        self.headline("Daten: {}".format(config.head))
        if config.desc:
            description = ET.SubElement(self.head, 'p')
            description.append(Generator.xmltext(config.desc))
        self.head.append(kwargs.get('dumplinks', None))
        self.table = ET.SubElement(self.main, 'table', attrib={'class': 'dumptable'})
        links = kwargs.get('links', None)
        if links is not None:
            self.head.append(links)
        section = ET.SubElement(self.head, 'section', attrib={'class': 'licenses'})
        if self.number_of_data_lists == 1:
            license_p = ET.SubElement(section, 'p')
            license_p.text = 'Quelle: '
            self.add_license(license_p, config.data_list[0].config)
        else:
            ET.SubElement(section, 'p').text = 'Quellen:'
            source_l = ET.SubElement(section, 'ul')
            for dl in config.data_list:
                li = ET.SubElement(source_l, 'li')
                li.text = dl.id + ": "
                self.add_license(li, dl.config)

    @classmethod
    def add_license(cls, target, data_obj):
        source = data_obj['source']
        source_link = source.get('url', None)
        source_element = ET.SubElement(target, 'span')
        if source_link is not None:
            source_element.tag = 'a'
            source_element.attrib = {'href': source_link}
        source_element.text = source['name']
        source_element.tail = ""
        if source.get('modified', False):
            source_element.tail += " (modifiziert)"
        lic = data_obj.get('license', None)
        if lic is not None:
            source_element.tail += ", © "
            lic_link = lic.get('url', None)
            lic_element = ET.Element('span')
            if lic_link is not None:
                lic_element.tag = 'a'
                lic_element.attrib = {'href': lic_link}
            target.append(lic_element)
            lic_element.text = lic['name']
            owner = lic.get('owner', None)
            if owner:
                lic_element.tail = " "
                owner_type = owner.get('type', None)
                owner_name = owner.get('name', '')
                if owner_type == 'twitter':
                    ET.SubElement(target, 'a', attrib={
                        'href': 'https://twitter.com/' + owner_name
                    }).text = "@{} auf twitter".format(owner_name)
                elif owner_type == 'name':
                    ET.SubElement(target, 'span').text = owner_name
                elif owner_type == 'link' and owner.get('url', False):
                    ET.SubElement(target, 'a', attrib={
                        'href': owner['url']
                    }).text = owner_name
                elif owner_type == 'github':
                    ET.SubElement(target, 'a', attrib={
                        'href': 'https://github.com/' + owner_name
                    }).text = "{} auf github".format(owner_name)

    def add_row(self, row):
        tr = ET.SubElement(self.table, 'tr')
        ET.SubElement(tr, 'th', attrib={'id': row[0]}).text = row[0]
        td = ET.SubElement(tr, 'td')
        lines = row[1].split('\\n')
        td.text = lines[0]
        for line in lines[1:]:
            br = ET.SubElement(td, 'br')
            br.tail = line
        if self.number_of_data_lists > 1:
            ET.SubElement(tr, 'td').text = row[3]
        # if more than one datalist, add column for which list this belongs to.
