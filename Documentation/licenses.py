"""Generates the copyright file with license information"""

from xml.etree import ElementTree as ET
from .markdowndoc import MarkdownDoc
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
        own = ET.SubElement(target, 'span')
        own.text = " "
        owner_type = owner.get('type', None)
        owner_name = owner.get('name', '')
        if owner_type == 'name':
            own.text += owner_name
        elif owner_type == 'twitter':
            ET.SubElement(target, 'a', attrib={
                'href': 'https://twitter.com/' + owner_name
            }).text = "@{} auf twitter".format(owner_name)
        elif owner_type == 'github':
            ET.SubElement(target, 'a', attrib={
                'href': 'https://github.com/' + owner_name
            }).text = "{} auf github".format(owner_name)
        elif owner_type == 'link' and owner.get('url', False):
            ET.SubElement(target, 'a', attrib={
                'href': owner['url']
            }).text = owner_name

def add_comments(target, comments):
    if len(comments) == 1:
        target.text = comments[0]
        return
    ul = ET.SubElement(target, 'ul')
    for c in comments:
        ET.SubElement(ul, 'li').text = c

class Licenses(MarkdownDoc):
    def __init__(self, mdfile, navi):
        super().__init__(mdfile, navi)
        lic_table = ET.SubElement(self.main, 'table')
        thead = ET.SubElement(lic_table, 'thead')
        tr = ET.SubElement(thead, 'tr')
        for text in ('', 'Beschreibung', 'Quelle', 'Lizenz',
                     'Anmerkungen', 'Dump', 'Magic Hashtag / Magic emoji'):
            th = ET.SubElement(tr, 'th')
            th.text = text
        self.lic = ET.SubElement(lic_table, 'tbody')

    def add_source(self, source):

        tr = ET.SubElement(self.lic, 'tr')
        nodl = len(source.data_list)
        rowspan = {}
        if nodl > 1:
            rowspan = {'rowspan': str(nodl)}
        ET.SubElement(tr, 'th', attrib=rowspan).text = ', '.join(
            set('{}{}:'.format(a.type, a.explicit_source) for a in source.access)
        )
        if source.desc:
            ET.SubElement(tr, 'td', attrib=rowspan).append(Generator.xmltext(source.desc))
        else:
            ET.SubElement(tr, 'td', attrib=rowspan).text = source.head
        for dl in source.data_list:
            add_source(ET.SubElement(tr, 'td'), dl.config['source'])
            license_container = ET.SubElement(tr, 'td')
            lic_obj = dl.config.get('license', None)
            if lic_obj:
                add_license(license_container, lic_obj)
            comments_container = ET.SubElement(tr, 'td', attrib={
                'style': 'text-align: left'
            })
            comments = dl.config.get('comments', None)
            if comments:
                add_comments(comments_container, comments)
            if dl == source.data_list[0]:
                dump_container = ET.SubElement(tr, 'td', attrib=rowspan)
                ET.SubElement(dump_container, 'a', attrib={
                    'href': '/dumps/' + source.id + '.html'
                }).text = source.id
                mht_container = ET.SubElement(tr, 'td', attrib=rowspan)
                mht_container.text = ', '.join(source.magic_hashtags)
                if source.id == 'bot':
                    mht_container.text = 'N/A'
            if not dl == source.data_list[-1]:
                tr = ET.SubElement(self.lic, 'tr')
