# -*- coding: utf-8 -*-

import sys
import csv
import plac
from lxml import objectify
from lxml.etree import fromstring, tostring
from lxml.etree import Element
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('epxml', 'templates'))


@plac.annotations(
    xml_in=('Schedule XML file',),
    template_name=('Name of rendering template',),
)
def conv(xml_in, html_out='out.html', template_name='standard.pt'):
    entries = get_entries(xml_in)
    template = env.get_template(template_name)
    html = template.render(entries=entries)
    with open(html_out, 'wb') as fp:
        fp.write(html.encode('utf8'))

def get_entries(xml_in):

    entries = list()

    id2title = dict()
    with open('msg.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            id2title[row[0]] = row[1]

    with open(xml_in, 'rb') as fp:
        xml = fp.read()

    root = fromstring(xml)
    for num, entry in enumerate(root.xpath('//entry')):
        title = Element('title')
        title.text = id2title[entry.attrib['id']]
        entry.append(title)
        entry_d = objectify.fromstring(tostring(entry))
        entries.append(entry_d)
    return entries

def main():
    plac.call(conv)

if __name__ == '__main__':
    main()

