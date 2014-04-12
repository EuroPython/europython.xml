# -*- coding: utf-8 -*-

import sys
import csv
import plac
import xmltodict
from lxml.etree import fromstring, tostring


def p(s):
    print >>sys.stdout, s.encode('utf-8')

@plac.annotations(
    xml_in=('Schedule XML file',)
)
def conv(xml_in):

    id2title = dict()
    with open('msg.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            id2title[row[0]] = row[1]

    with open(xml_in, 'rb') as fp:
        xml = fp.read()

    root = fromstring(xml)

    p(u'<table id="talks" border="1">')
    p(u'<tbody>')

    for num, entry in enumerate(root.xpath('//entry')):

        print '-'*80
        print tostring(entry)

        entry_d = xmltodict.parse(tostring(entry))
        entry_id = entry_d['entry']['@id']

        p(u'<tr>')

        p(u'<td>')
        p(u'{}'.format(num+1))
        p(u'</td>')

        # Topic(s)
        p(u'<td>')
        for topic in entry.xpath('topics/topic'):
            name = topic.xpath('text()')
            if name: 
                p(u'<div>{}</div>'.format(name[0]))
        p(u'</td>')

        # Speaker(s)
        p(u'<td>')
        for speaker in entry.xpath('speakers/speaker'):
            name = speaker.xpath('name/text()')
            if name: 
                p(u'<div class="name">{}</<div>'.format(name[0]))
                profile = speaker.xpath('profile/text()')
#            if profile:
#                p(u'<div class="profile">{}</<div>'.format(profile[0]))
        p(u'</td>')

        # Title
        p(u'<td>')
        p(u'{}'.format(id2title[entry_id]))
        p(u'</td>')

        p(u'</tr>')

    p(u'</tbody>')
    p(u'</table>')

def main():
    plac.call(conv)

if __name__ == '__main__':
    main()

