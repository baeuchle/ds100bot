"""Creates a source dump HTML file"""

from xml.etree import ElementTree as ET
from .generator import Generator

class Dump(Generator):
    def __init__(self, titletext, config, **kwargs):
        super().__init__(titletext, **kwargs)
        self.headline("Daten aus Quelle {}".format(config.head))
        if config.desc:
            description = ET.SubElement(self.head, 'p')
            description.text = config.desc
        self.head.append(kwargs.get('dumplinks', None))
        self.table = ET.SubElement(self.main, 'table', attrib={'class': 'dumptable'})
        links = kwargs.get('links', None)
        if links is not None:
            self.head.append(links)
        # now, also include license information.

    def add_row(self, row):
        tr = ET.SubElement(self.table, 'tr')
        th = ET.SubElement(tr, 'th', attrib={'id': row[0]})
        th.text = row[0]
        td = ET.SubElement(tr, 'td')
        lines = row[1].split('\\n')
        td.text = lines[0]
        for line in lines[1:]:
            br = ET.SubElement(td, 'br')
            br.tail = line
