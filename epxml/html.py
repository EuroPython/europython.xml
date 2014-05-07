# -*- coding: utf-8 -*-

import sys
import plac
from jinja2 import Environment, PackageLoader
import util


env = Environment(loader=PackageLoader('epxml', 'templates'))

class View(object):

    def markdown(self, text):
        return markdown2.markdown(unicode(text))


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    template_name=('Name of rendering template', 'option', 't'),
    html_out=('Output filename', 'option', 'o'),
    xpath_filter=('XPath filter', 'option', 'x')
    )
def conv(xml_in, html_out='out.html', template_name='html.pt', xpath_filter='//entry'):

    if not xml_in:
        raise ValueError('No XML input file specified (-i|--xml-in)')

    entries = util.get_entries(xml_in, xpath_filter)
    template = env.get_template(template_name)
    html = template.render(entries=entries,
            view=util.JinjaView())
    with open(html_out, 'wb') as fp:
        fp.write(html.encode('utf8'))
    return html_out


def main():
    plac.call(conv)


if __name__ == '__main__':
    main()

