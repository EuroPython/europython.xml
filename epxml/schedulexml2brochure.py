# -*- coding: utf-8 -*-

import sys
import plac
from jinja2 import Environment, PackageLoader
import util
import loremipsum



env = Environment(loader=PackageLoader('epxml', 'templates'))

class View(object):

    def demo(self):
        return (u'/'.join([p[2] for p in loremipsum.Generator().generate_paragraphs(1)]))


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    html_out=('Output HTML file', 'option', 'o'),
    )
def conv(xml_in, html_out='brochure.html'):
    entries_d1 = util.get_entries(xml_in, '//day[@date="2014-07-22"]/entry')
    entries_d2 = util.get_entries(xml_in, '//day[@date="2014-07-23"]/entry')
    entries_d3 = util.get_entries(xml_in, '//day[@date="2014-07-24"]/entry')
    template = env.get_template('brochure.pt')
    html = template.render(
            d1=dict(entries=entries_d1, date_str='22/07/2014'),
            d2=dict(entries=entries_d2, date_str='23/07/2014'),
            d3=dict(entries=entries_d3, date_str='24/07/2014'),
            view=View())
    with open(html_out, 'wb') as fp:
        fp.write(html.encode('utf8'))


def main():
    plac.call(conv)


if __name__ == '__main__':
    main()

