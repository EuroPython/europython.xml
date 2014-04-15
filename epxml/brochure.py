# -*- coding: utf-8 -*-

import os
import sys
import plac
import subprocess
from datetime import timedelta
from datetime import datetime
from jinja2 import Environment, PackageLoader
import util


env = Environment(loader=PackageLoader('epxml', 'templates'))


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    html_out=('Output HTML file', 'option', 'o'),
    pdf_converter=('Generate PDF output using prince or pdfreactor', 'option', 'p')
    )
def conv(xml_in=None, html_out='brochure.html', pdf_converter=None):

    if not xml_in:
        raise ValueError('No XML input file specified (-i|--xml-in)')

    entries = list()
    for day in range(22, 25):
        date_str = '2014-07-{}'.format(day)
        entries.append(dict(entries=util.get_entries(xml_in, '//day[@date="{}"]/entry'.format(date_str)),
                            date_str=date_str))

    template = env.get_template('brochure.pt')
    html = template.render(
            day_entries=entries,
            view=util.JinjaView())
    with open(html_out, 'wb') as fp:
        print 'HTML output written to "{}"'.format(html_out)
        fp.write(html.encode('utf8'))

    if pdf_converter in ('prince', 'pdfreactor'):
        out_pdf = '{}.pdf'.format(os.path.splitext(html_out)[0])
        if pdf_converter == 'prince':
            cmd = 'prince9 -v "{}" -o "{}"'.format(html_out, out_pdf)
        elif pdf_converter == 'pdfreactor':
            cmd = 'pdfreactor "{}" "{}"'.format(html_out, out_pdf)
        print 'Running: {}'.format(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        status = proc.wait()
        print 'Exit code: {}'.format(status)
        print 'PDF written to "{}"'.format(out_pdf)


def main():
    plac.call(conv)


if __name__ == '__main__':
    main()
