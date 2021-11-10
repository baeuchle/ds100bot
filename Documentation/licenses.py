"""Generates the copyright file with license information"""

from xml.etree import ElementTree as ET
from .markdowndoc import MarkdownDoc
from .generator import Generator

class Licenses(MarkdownDoc):
    def __init__(self, mdfile, navi):
        super().__init__(mdfile, navi)
        self.add_table('Nach id sortiert')

    def add_table(self, headline):
        lic_table = ET.SubElement(self.main, 'table')
        if headline:
            ET.SubElement(lic_table, 'caption').text = headline
        thead = ET.SubElement(lic_table, 'thead')
        tr = ET.SubElement(thead, 'tr')
        for text in ('', 'Beschreibung',
                     'Dump', 'Magic Hashtag / Magic emoji'):
            th = ET.SubElement(tr, 'th')
            th.text = text
        self.lic = ET.SubElement(lic_table, 'tbody')

    def add_source(self, source):
        tr = ET.SubElement(self.lic, 'tr')
        ET.SubElement(tr, 'th').text = ', '.join(
            set('{}{}:'.format(a.type, a.explicit_source) for a in source.access)
        )
        if source.desc:
            ET.SubElement(tr, 'td').append(Generator.xmltext(source.desc))
        else:
            ET.SubElement(tr, 'td').text = source.head
        dump_container = ET.SubElement(tr, 'td')
        ET.SubElement(dump_container, 'a', attrib={
            'href': '/dumps/' + source.id + '.html'
        }).text = source.id
        mht_container = ET.SubElement(tr, 'td')
        mht_container.text = ', '.join(source.magic_hashtags)
        if source.id == 'bot':
            mht_container.text = 'N/A'
