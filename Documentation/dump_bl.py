"""Creates the dump of the Blacklist"""

from xml.etree import ElementTree as ET
from .dump import Dump
from .generator import Generator

class DumpBlacklist(Dump):
    def __init__(self, **kwargs):
        # pylint: disable=W0233
        Generator.__init__(self, 'DS100-Daten-Dump Blacklist', **kwargs)
        self.headline("Blacklist")
        ET.SubElement(self.head, 'p').text = """Die folgenden Einträge werden nicht ohne explizite
        Quellenangabe (z.B. "#DS:") beantwortet."""
        self.head.append(kwargs.get('dumplinks', None))
        self.table = ET.SubElement(self.main, 'table', attrib={'class': 'dumptable'})
        links = kwargs.get('links', None)
        if links is not None:
            self.head.append(links)
        self.number_of_data_lists = 2
