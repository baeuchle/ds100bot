"""Base class for all HTML documentation generators"""

from xml.etree import ElementTree as ET

class Generator:
    def __init__(self, titletext, **kwargs):
        self.html = ET.Element('html')
        head = ET.SubElement(self.html, 'head')
        head.append(ET.Element('meta', attrib={'charset': 'utf-8'}))
        head.append(ET.Element('meta', attrib={
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }))
        head.append(ET.Element('link', attrib={
            'rel': 'stylesheet',
            'type': 'text/css',
            'href': '/bot.css'
        }))
        head.append(ET.Element('link', attrib={
            'rel': 'shortcut icon',
            'type': 'image/svg+xml',
            'href': 'https://avatar.frankfurtium.de/ds100.svg'
        }))
        title = ET.SubElement(head, 'title')
        title.text = titletext
        body = ET.SubElement(self.html, 'body')
        self.head = ET.SubElement(body, 'header')
        self.main = ET.SubElement(body, 'main')
        self.navi = ET.SubElement(body, 'nav')
        self.foot = ET.SubElement(body, 'footer')
        if 'links' in kwargs:
            self.navi.append(kwargs['links'])

    def headline(self, titletext):
        head = ET.SubElement(self.head, 'h1')
        head.text = titletext

    def write(self, targetfile):
        with targetfile.open(mode='w') as tf:
            ET.ElementTree(self.html).write(tf,
                encoding='unicode', method='xml')
