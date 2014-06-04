# -*- coding: utf-8 -*-

import os
import sys
import plac
import operator
import subprocess
import tempfile
import pkg_resources
import shutil
from datetime import timedelta
from datetime import datetime
from jinja2 import Environment, PackageLoader
from pp.client.python.pdf import pdf        
import util


env = Environment(loader=PackageLoader('epxml', 'templates'))


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    html_out=('Output HTML file', 'option', 'o'),
    first_page_number=('Start with page number XX', 'option', 'n'),
    pdf_converter=('Generate PDF output using prince or pdfreactor (princexml, remote-princexml, pdfreactor, remote-pdfreactor)', 'option', 'p'),
    pdf_filename=('Custom PDF output filename', 'option', 'f'),
    template=('Rendering template (default: brochure_talks.pt)', 'option', 't'),
    imagedir=('Directory containing speaker images', 'option', 'z'),
    fontpath=('Directory containing fonts', 'option', 'y')
    )
def conv(xml_in=None, 
        html_out='brochure.html', 
        first_page_number=1, 
        pdf_converter=None, 
        pdf_filename=None, 
        imagedir=None,
        fontpath='fonts',
        template='brochure_talks.pt'):

    if not xml_in:
        raise ValueError('No XML input file specified (-i|--xml-in)')

    entries = list()
    for day in range(21, 25):
        date_str = '2014-07-{}'.format(day)
        entries_d = util.get_entries(xml_in, '//day[@date="{}"]/entry'.format(date_str))
        entries_d = [e for e in entries_d if e.category not in ['LUNCH']]
        entries.append(dict(entries=entries_d,
                            date_text=datetime.strptime(date_str, '%Y-%m-%d').strftime('%A'),
                            date_str=date_str))

    speakers = list()
    speakers_seen = set()
    for e in util.get_entries(xml_in, '//day/entry'):
        for speaker in e.speakers or []:
            speaker_name = speaker.speaker.name
            speaker_description = speaker.speaker.description
            speaker_image_url = speaker.speaker.image
            speaker_image_file = ''
            speaker_image_found = False
            if imagedir:
                speaker_image_file = os.path.join(os.path.abspath(imagedir), speaker.speaker.attrib['id'])
                for ext in ('.png', '.jpg', '.gif'):
                    if os.path.exists(speaker_image_file + ext):
                        speaker_image_file += ext
                        speaker_image_found = True
                        break

            if not speaker_image_found:
                print 'No speaker image found for {} ({})'.format(speaker_name.text.encode('utf8'), speaker.speaker.attrib['id'])

            if not speaker_name in speakers_seen:
                speakers.append(dict(name=speaker_name,
                                    name_lower=unicode(speaker_name).lower(),
                                    description=speaker_description,
                                    image_file=speaker_image_file,
                                    has_image=speaker_image_found,
                                    image_url=speaker_image_url))
                speakers_seen.add(speaker_name)

    speakers = sorted(speakers, key=operator.itemgetter('name_lower'))
    print '{} speakers found'.format(len(speakers))

    template = env.get_template(template)
    html = template.render(
            first_page_number=int(first_page_number) - 1,
            day_entries=entries,
            speakers=speakers,
            view=util.JinjaView())

    with open(html_out, 'wb') as fp:
        print 'HTML output written to "{}"'.format(html_out)
        fp.write(html.encode('utf8'))

    if pdf_converter in ('princexml', 'pdfreactor', 'remote-princexml', 'remote-pdfreactor'):

        # write HTML file to a dedicated scratch directory
        tmpd = tempfile.mkdtemp()
        html_filename  = os.path.join(tmpd, 'index.html')
        with open(html_filename, 'wb') as fp:
            fp.write(html.encode('utf-8'))

        # copy over conversion resources
        resources_dir = os.path.join(os.path.dirname(__file__), 'templates', 'resources')
        for dirname, dirnames, filenames in os.walk(resources_dir):
            for fname in filenames:
                shutil.copy(os.path.join(dirname, fname), tmpd)

        if fontpath and os.path.exists(fontpath):
            for filename in os.listdir(fontpath):
                shutil.copy(os.path.join(fontpath, filename), tmpd)

        if pdf_converter in ('princexml', 'pdfreactor'):
            # local pdf generation through PrinceXML or PDFreactor

            if pdf_filename:
                out_pdf = pdf_filename
            else:
                out_pdf = '{}.pdf'.format(os.path.splitext(html_filename)[0])
            if pdf_converter == 'princexml':
                cmd = 'prince -v "{}" -o "{}"'.format(html_filename, out_pdf)
            elif pdf_converter == 'pdfreactor':
                cmd = 'pdfreactor "{}" "{}"'.format(html_filename, out_pdf)
            print 'Running: {}'.format(cmd)
            proc = subprocess.Popen(cmd, shell=True)
            status = proc.wait()
            print 'Exit code: {}'.format(status)
            if status != 0:
                raise RuntimeError('PDF generation failed')
            print 'PDF written to "{}"'.format(out_pdf)
            return out_pdf

        elif pdf_converter in ('remote-princexml', 'remote-pdfreactor'):
            # remote pdf generation through PrinceXML or PDFreactor
            # through https://pp-server.zopyx.com

            server_url = os.environ['PP_SERVER_URL']
            authorization_token = os.environ['PP_AUTHORIZATION_TOKEN']
            output_filename = tempfile.mktemp(suffix='.pdf', dir=tmpd)
            result = pdf(source_directory=tmpd,
                         converter=pdf_converter.replace('remote-', ''),
                         output=output_filename,
                         server_url=server_url,
                         authorization_token=authorization_token,
                         verbose=True)

            if result['status'] != 'OK':
                raise RuntimeError('Remote PDF generation failed')

            print 'PDF written to "{}"'.format(result['output_filename'])
            return result['output_filename']


def main():
    plac.call(conv)


if __name__ == '__main__':
    main()
