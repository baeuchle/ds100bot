"""Base class for all HTML documentation generators"""

from xml.etree import ElementTree as ET

class Generator:
    SITENAME = {'property': 'og:site_name', 'content': 'DS100 Bot'}
    CARD = {'content': 'https://ds100.frankfurtium.de/socialcard.png'}
    LOCALE = {'property': 'og:locale', 'content': 'de_DE'}
    CARDTYPE = {'name': 'twitter:card', 'content': 'summary_large_image'}
    SITE = {'name': 'twitter:site', 'content': '@_ds_100'}
    CREATOR = {'name': 'twitter:creator', 'content': '@baeuchle'}
    def __init__(self, titletext, **kwargs):
        self.html = ET.Element('html', attrib={'prefix': 'og: https://ogp.me/ns#'})
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
        ET.SubElement(head, 'script', attrib={
            'type': 'text/javascript',
            'src': '/script.js'
        }).text = " "
        desc = {'content': kwargs.get('desc', titletext)}
        head.append(ET.Element('meta', attrib={'property': 'og:title', 'content': titletext}))
        head.append(ET.Element('meta', attrib=Generator.SITENAME))
        head.append(ET.Element('meta', attrib={'property': 'og:image', **Generator.CARD}))
        head.append(ET.Element('meta', attrib={'property': 'og:description', **desc}))
        head.append(ET.Element('meta', attrib=Generator.LOCALE))
        head.append(ET.Element('meta', attrib=Generator.CARDTYPE))
        head.append(ET.Element('meta', attrib={'name': 'twitter:title', 'content': titletext}))
        head.append(ET.Element('meta', attrib={'name': 'twitter:description', **desc}))
        head.append(ET.Element('meta', attrib=Generator.SITE))
        head.append(ET.Element('meta', attrib=Generator.CREATOR))
        head.append(ET.Element('meta', attrib={'name': 'twitter:image', **Generator.CARD}))
        head.append(ET.Element('meta', attrib={'name': 'description', **desc}))
        title = ET.SubElement(head, 'title')
        title.text = titletext
        body = ET.SubElement(self.html, 'body')
        self.head = ET.SubElement(body, 'header')
        ET.SubElement(body, 'p').append(Generator.xmltext("""
     Zeige Passagen, die speziell für…
     <input type="checkbox" name="show_selector" value="twitter" id="show_tw" checked="checked" onclick="toggle_show(this)" />
     <label for="show_tw">Twitter</label>
     <input type="checkbox" name="show_selector" value="mastodon" id="show_ma" checked="checked"  onclick="toggle_show(this)" />
     <label for="show_ma">Mastodon</label>
     … sind."""))
        self.main = ET.SubElement(body, 'main')
        self.foot = ET.SubElement(body, 'footer')
        self.navi = ET.SubElement(self.foot, 'navi')
        if 'links' in kwargs:
            ET.SubElement(self.navi, 'p').text = 'Links'
            self.navi.append(kwargs['links'])

    def headline(self, titletext):
        ET.SubElement(self.head, 'h1').text = titletext

    def write(self, targetfile):
        with targetfile.open(mode='w') as tf:
            ET.ElementTree(self.html).write(tf,
                encoding='unicode', method='xml')

    @classmethod
    def xmltext(cls, text):
        return ET.fromstring('<span>' + text + '</span>')
