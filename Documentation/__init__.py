"""Collects everything for the successful creation of HTML Documentation"""

from xml.etree import ElementTree as ET
from pathlib import Path
from .generator import Generator
from .dump import Dump
from .dump_il import DumpIgnorelist
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
    div = ET.Element('div', attrib={'class': 'dumpnavi hiddennavi'})
    ET.SubElement(div, 'div', attrib={'class': 'closenavi'},
        onclick="toggle_any('dumpnavi')").text = "Alle Dumps"
    linklist = ET.SubElement(div, 'ul')
    sublists = {}
    sigils = {'#': 'Orte',
              '$': 'Strecken',
              '/': 'Linien',
              '%': 'Signale',
              '&': 'Regeln'
             }
    for sigil, sigilname in sigils.items():
        sublists[sigil] = ET.Element('ul', attrib={'class': f'dump_{sigilname.lower()}'})
    for cid, conf in sorted(config_list.items()):
        item = ET.Element('li')
        ET.SubElement(item, 'a', attrib={'href': '/dumps/' + cid + '.html'}).text = conf.head
        if len(conf.file.stem) > 5:
            inserted_once = False
            for sigil in set(x.type for x in conf.access):
                if sigil in sublists:
                    sublists[sigil].append(item)
                    inserted_once = True
            if inserted_once:
                continue
        # Fallthrough from the above: 5 letters or less or unknown sigil.
        linklist.append(item)
    for sigil, subl in sublists.items():
        classname = f'dump_{sigils[sigil].lower()}'
        sublistitem = ET.SubElement(linklist, 'li', attrib={'class': f'{classname} hiddennavi'})
        listhl = ET.SubElement(sublistitem, 'div', onclick=f"toggle_any('{classname}')")
        ET.SubElement(listhl, 'span', attrib={'class': 'sigil'}).text = sigil
        ET.SubElement(listhl, 'span').text = sigils[sigil]
        sublistitem.append(subl)
    item = ET.SubElement(linklist, 'li')
    ET.SubElement(item, 'a', attrib={'href': '/dumps/ignorelist.html'}).text = 'Blacklist'
    return div

def navilink_list(version):
    linkroot = ET.parse('doc/links.snip').getroot()
    for vtag in linkroot.findall(".//li[@class='transform_version']"):
        vtag.text = "Version: {}".format(version)
    return linkroot

def create_dump_mainpage(navi, dump, dumpdir):
    mp = Generator('DS100-Daten-Dump Liste', links=navi)
    mp.headline('Liste der Datenquellen')
    dl = ET.SubElement(mp.main, 'navi')
    # We will manipulate dump, so we have to copy it first.
    # This is the only way I can find.
    dl.append(ET.fromstring(ET.tostring(dump)))
    dl.find('./div').set('class', 'bigdumplist')
    mp.write(dumpdir / 'index.html')

def dump_source(config, dumplinks, navilinks, db, dumpdir):
    dump = Dump('DS100-Daten-Dump', config, dumplinks=dumplinks, links=navilinks)
    for entry_row in db.dumplist(config.id):
        dump.add_row(entry_row)
    dump.write(dumpdir / (config.id + '.html'))

def dump_ignorelist(dumplinks, navilinks, db, dumpdir):
    dump = DumpIgnorelist(dumplinks=dumplinks, links=navilinks)
    for entry_row in db.dumpblack():
        dump.add_row(entry_row)
    dump.write(dumpdir / 'ignorelist.html')
