# -*- coding: utf-8 -*-

import sys
import csv
from lxml.etree import fromstring, tostring
from lxml import objectify

def p(s):
    print >>sys.stdout, s.encode('utf-8')

id2title = dict()
with open('msg.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        id2title[row[0]] = row[1]

xml = open('accepted.xml', 'rb').read()
root = fromstring(xml)
tree = objectify.fromstring(xml)

p(u'<table id="talks" border="1">')
p(u'<tbody>')

for num, entry in enumerate(root.xpath('//entry')):

    entry_id = entry.attrib['id']

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
