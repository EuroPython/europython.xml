import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'setuptools',
    'jinja2',
    'markdown2',
    'lxml',
    'loremipsum',
    'plac',
]

setup(name='europython.xml',
      version='0.1',
      description='EuroPython 2014 talks XML management',
      long_description='',
      classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        ],
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/pp.client-python',
      keywords='python',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      entry_points="""\
      [console_scripts]
      schedulexml2html=epxml.html:main
      schedulexml2brochure=epxml.brochure:main
      """,
      )
