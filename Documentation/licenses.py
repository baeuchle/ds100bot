"""Generates the copyright file with license information"""

from xml.etree import ElementTree as ET
from .markdowndoc import MarkdownDoc

class Licenses(MarkdownDoc):
    def __init__(self, mdfile, navi):
        super().__init__(mdfile, navi)
        lic_table = ET.SubElement(self.main, 'table')
        thead = ET.SubElement(lic_table, 'thead')
        tr = ET.SubElement(thead, 'tr')
        for text in ('', 'Beschreibung', 'Quelle', 'Lizenz',
                     'Anmerkungen', 'Dump', 'Magic Hashtag'):
            th = ET.SubElement(tr, 'th')
            th.text = text
        self.lic = ET.SubElement(lic_table, 'tbody')

    def add_source(self, source):
        tr = ET.SubElement(self.lic, 'tr')
        td = ET.SubElement(tr, 'td')
        td.text = str(source)
