"""Generates an arbitrary HTML documentation file from a Markdown file"""

from xml.etree import ElementTree as ET
import markdown
from .generator import Generator

class MarkdownDoc(Generator):
    def __init__(self, mdfile, navi):
        with mdfile.open() as mdin:
            self.md = mdin.read()
        # wrap in <markdown> so that the XML parser is satisfied
        hypertext = '<markdown>{}</markdown>'.format(markdown.markdown(self.md))
        xmltree = ET.fromstring(hypertext)
        hl = xmltree.find('./h1')
        title = '@_ds_100'
        if hl is not None:
            title += ': ' + hl.text
        super().__init__(title, links=navi)
        self.head.append(hl)
        for tag in xmltree:
            if tag.tag == 'h1':
                continue
            self.main.append(tag)
