"""Collects everything for the successful creation of HTML Documentation"""

from xml.etree import ElementTree as ET
from pathlib import Path
from .generator import Generator
from .dump import Dump
from .markdowndoc import MarkdownDoc
from .licenses import Licenses

def create_documentation(navi_list, md_dir, html_dir):
    for mdfile in md_dir.glob('*.md'):
        # don't consider copyright.md:
        if mdfile.stem == 'copyright':
            continue
        dp = MarkdownDoc(mdfile, navi_list)
        dp.write(html_dir / (mdfile.stem + '.html'))

def dumplink_list(config_list):
    linklist = ET.Element('ul', attrib={'class': 'flat'})
    item = ET.SubElement(linklist, 'li')
    item.text = "Alle Quellen:"
    item = ET.SubElement(linklist, 'li')
    link = ET.SubElement(item, 'a', attrib={'href': '/dumps/blacklist.html'})
    link.text = 'Blacklist'
    for cid, conf in sorted(config_list.items()):
        item = ET.SubElement(linklist, 'li')
        link = ET.SubElement(item, 'a', attrib={'href': '/dumps/' + cid + '.html'})
        link.text = conf.head
    return linklist

def navilink_list(version):
    linkroot = ET.parse('doc/links.snip').getroot()
    for vtag in linkroot.findall("li[@class='transform_version']"):
        vtag.text = "Version: {}".format(version)
    return linkroot

def create_dump_mainpage(navi, dump, dumpdir):
    mp = Generator('DS100-Daten-Dump Liste', links=navi)
    mp.headline('Liste der Datenquellen')
    mp.main.append(dump)
    mp.write(dumpdir / 'index.html')

def dump_source(config, dumplinks, navilinks, db, dumpdir):
    dump = Dump('DS100-Daten-Dump', config, dumplinks=dumplinks, links=navilinks)
    for entry_row in db.dumplist(config.id):
        dump.add_row(entry_row)
    dump.write(dumpdir / (config.id + '.html'))
