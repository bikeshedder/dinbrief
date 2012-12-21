#!/usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Prevent "TypeError: 'NoneType' object is not callable" when running tests.
# (http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

from dinbrief import __version__ as package_version

setup(
    name='dinbrief',
    version=package_version,
    description='PDF renderer for DIN 5008 and DIN 676 compliant letters and invoices',
    long_description=read('README'),
    author='Michael P. Jung',
    author_email='michael.jung@terreon.de',
    license='BSD',
    keywords='dinbrief DIN 5008 676 brief letter invoice pdf',
    url='https://bitbucket.org/terreon/dinbrief',
    packages=['dinbrief', 'dinbrief.invoice'],
    #test_suite='dinbrief.tests',
    install_requires=read('requirements.txt').split('\n'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
