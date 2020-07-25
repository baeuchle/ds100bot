"""Creates a source dump HTML file"""

from xml.etree import ElementTree as ET
from .generator import Generator
from .licenses import add_source, add_license

def add_source_line(target, data_obj):
    add_source(target, data_obj['source'])
    lic = data_obj.get('license', None)
    if lic is not None:
        ET.SubElement(target, 'span').text = ", "
        add_license(target, lic)

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
            add_source_line(license_p, config.data_list[0].config)
        else:
            ET.SubElement(section, 'p').text = 'Quellen:'
            source_l = ET.SubElement(section, 'ul')
            for dl in config.data_list:
                li = ET.SubElement(source_l, 'li')
                ET.SubElement(li, 'strong').text = dl.id
                ET.SubElement(li, 'span').text = ": "
                add_source_line(li, dl.config)

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
