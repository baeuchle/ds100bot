"""Creates a source dump HTML file"""

from xml.etree import ElementTree as ET
from .generator import Generator

def add_source(target, source):
    source_link = source.get('url', None)
    source_element = ET.SubElement(target, 'span')
    if source_link is not None:
        source_element.tag = 'a'
        source_element.attrib = {'href': source_link}
    source_element.text = source['name']
    if source.get('modified', False):
        ET.SubElement(target, 'span').text = " (modifiziert)"

def add_owner(element, owner):
    own = ET.SubElement(element, 'span')
    own.text = " "
    owner_type = owner.get('type', None)
    owner_name = owner.get('name', '')
    if owner_type == 'name':
        own.text += owner_name
    elif owner_type == 'twitter':
        ET.SubElement(element, 'a', attrib={
            'href': 'https://twitter.com/' + owner_name
        }).text = "@{} auf twitter".format(owner_name)
    elif owner_type == 'github':
        ET.SubElement(element, 'a', attrib={
            'href': 'https://github.com/' + owner_name
        }).text = "{} auf github".format(owner_name)
    elif owner_type == 'link' and owner.get('url', False):
        ET.SubElement(element, 'a', attrib={
            'href': owner['url']
        }).text = owner_name

def add_license(target, lic):
    ET.SubElement(target, 'span').text = "© "
    lic_link = lic.get('url', None)
    lic_element = ET.Element('span')
    if lic_link:
        lic_element.tag = 'a'
        lic_element.attrib = {'href': lic_link}
    target.append(lic_element)
    lic_element.text = lic['name']
    owner = lic.get('owner', None)
    if owner:
        add_owner(target, owner)
    contributors = lic.get('contributors', None)
    if contributors:
        contrib = ET.SubElement(target, 'strong')
        contrib.text = " Beitragende:"
        for c in contributors:
            add_owner(target, c)

def add_comments(target, comments):
    if len(comments) == 1:
        target.text = comments[0]
        return
    ul = ET.SubElement(target, 'ul')
    for c in comments:
        ET.SubElement(ul, 'li').text = c

def add_source_line(target, data_obj):
    add_source(target, data_obj['source'])
    lic = data_obj.get('license', None)
    if lic is not None:
        ET.SubElement(target, 'span').text = ", "
        add_license(target, lic)

class Dump(Generator):
    def __init__(self, titletext, config, **kwargs):
        super().__init__(titletext,
                         desc='Liste aller Abkürzungen in der Quelle {}'.format(config.head),
                         **kwargs)
        self.number_of_data_lists = len(config.data_list)
        self.headline("Daten: {}".format(config.head))
        if config.desc:
            description = ET.SubElement(self.head, 'p')
            description.append(Generator.xmltext(config.desc))
        dlnavi = ET.SubElement(self.head, 'navi')
        ET.SubElement(dlnavi, 'p', onclick="toggle_any('dumpnavi')").text = 'Alle Dumps'
        dlnavi.append(kwargs.get('dumplinks', None))
        self.table = ET.SubElement(self.main, 'table', attrib={'class': 'dumptable'})
        section = ET.SubElement(self.head, 'section', attrib={'class': 'licenses'})
        if self.number_of_data_lists == 1:
            license_p = ET.SubElement(section, 'p')
            license_p.text = 'Quelle: '
            add_source_line(license_p, config.data_list[0].config)
            comments = config.data_list[0].config.get('comments', None)
            if comments:
                ET.SubElement(license_p, 'br')
                if len(comments) == 1:
                    comment_p = ET.SubElement(license_p, 'span')
                else:
                    comment_p = ET.SubElement(license_p, 'div')
                add_comments(comment_p, comments)
        else:
            ET.SubElement(section, 'p').text = 'Quellen:'
            source_l = ET.SubElement(section, 'ul')
            for dl in config.data_list:
                li = ET.SubElement(source_l, 'li')
                ET.SubElement(li, 'strong').text = dl.id
                ET.SubElement(li, 'span').text = ": "
                add_source_line(li, dl.config)
                comments = dl.config.get('comments', None)
                if comments:
                    ET.SubElement(li, 'br')
                    comment_p = ET.SubElement(li, 'span')
                    add_comments(comment_p, comments)

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
