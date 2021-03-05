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
        generator_kwargs = {'links': navi}
        xmltree = ET.fromstring(hypertext)
        hl = xmltree.find('./h1')
        title = '@_ds_100'
        if hl is not None:
            title += ': ' + hl.text
        # title is overridden by p[@id=meta]/title:
        meta = xmltree.find('p[@id="meta"]')
        if meta:
            xmltree.remove(meta)
            titletag = meta.find('./title')
            if titletag is not None:
                title = titletag.text
            desc = meta.find('./desc')
            if desc is not None:
                generator_kwargs['desc'] = desc.text
        super().__init__(title, **generator_kwargs)
        self.head.append(hl)
        for tag in xmltree:
            if tag.tag == 'h1':
                continue
            self.main.append(tag)
