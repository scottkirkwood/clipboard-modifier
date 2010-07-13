#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

NAME = 'clipboard-modifier'
VER = '0.2.1'
DIR = 'clipboardmodifier'
PY_NAME = 'clipboardmodifier'
DEB_NAME = NAME.replace('-', '')
RELEASE_FILE = 'CHANGELOG.txt'
RELEASE_FORMAT=r'Version (?P<ver>[^ ]+) \((?P<date>[^)]+)\)'

PY_SRC = '%s.py' % PY_NAME
DEPENDS = []
DEPENDS_STR = ' '.join(DEPENDS)

MENU_SUBSECTION = 'Util'
AUTHOR_NAME = 'Scott Kirkwood'
COPYRIGHT_NAME = 'Google Inc.'
GOOGLE_CODE_EMAIL = 'scott@forusers.com'
MAN_FILE = 'man/%s.1' % NAME
DESKTOP_FILE = 'icons/%s.desktop' % NAME
ICON = 'icons/%s.xpm' % NAME
COMMAND = '/usr/bin/%s' % NAME

SETUP = dict(
    name=NAME,
    version=VER,
    description="Change your clipboard text in a variety of ways.",
    long_description=
"""A flexible system to modify the text in a clipboard in a variety of ways.
Out of the box we have:
  * Copy a spreadsheet and change the clipboard so that it can be pasted into a
  * wiki, with vertical bars (|) instead of tabs.  Modify your multi-line clipboard text so that it can be pasted into Java or Python as strings.
  * Modify an URL in the clipboard pointing to Amazon so that it has your Associate ID in it. 
  * Run a shell command piping the clipboard to it and retrieving the output from it.
  * Force a clibpboard to text (removing formatting, etc.).
  * Convert a complicated url into it's python equivalent, using urlencode.
  * And many more...

It uses wxPython and when you bring it's window to the front it modifies
the clipboard with the currently selected utility.
""",
    author=AUTHOR_NAME,
    author_email='scott@forusers.com',
    url='http://code.google.com/p/%s/' % NAME,
    download_url='http://%s.googlecode.com/files/%s-%s.zip' % (NAME, NAME, VER),
    keywords=['clipboard', 'utility', 'wxPython', 'Python'],
    packages=['clipboardmodifier', 'clipboardmodifier/plugins'],
    scripts=['scripts/clipboard-modifier'],
    license='Apache 2.0',
    platforms=['POSIX', 'Windows'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)

if __name__ == '__main__':
  setup(**SETUP)
