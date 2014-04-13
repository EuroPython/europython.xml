# -*- coding: utf-8 -*-

import os
import sys
import plac
import subprocess
from datetime import timedelta
from datetime import datetime
import loremipsum
import markdown2
from jinja2 import Environment, PackageLoader
import util


env = Environment(loader=PackageLoader('epxml', 'templates'))

class View(object):

    def demo(self):
        return (u'/'.join([p[2] for p in loremipsum.Generator().generate_paragraphs(1)]))

    def time(self, entry):
        hours_start = int(entry.start / 100 )
        minutes_start = int(entry.start % 100)
        duration = int(entry.duration)
        start = datetime(2000, 1, 1, hours_start, minutes_start)
        end = start + timedelta(minutes=duration)
        return '{:02d}:{:02d} - {:02d}:{:02d}h'.format(start.hour, start.minute, end.hour, end.minute)

    def markdown(self, text):
        return markdown2.markdown(unicode(text))


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    html_out=('Output HTML file', 'option', 'o'),
    pdf_converter=('Generate PDF output using prince or pdfreactor', 'option', 'p')
    )
def conv(xml_in, html_out='brochure.html', pdf_converter=None):
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

