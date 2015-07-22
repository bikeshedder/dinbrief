#!/usr/bin/env python

import os
from setuptools import setup
from setuptools.command.install_lib import install_lib as _install_lib
from distutils.command.build import build as _build
from distutils.cmd import Command

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

# The following compile_translations, build and install_lib command
# classes were taken from http://stackoverflow.com/a/15520651/994342
# and adapted to Django 1.8.
class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        from django.core.management.commands.compilemessages import Command as CompileMessagesCommand
        curdir = os.getcwd()
        os.chdir(os.path.realpath('dinbrief'))
        cmd = CompileMessagesCommand()
        cmd.handle(verbosity=1, exclude=[])
        os.chdir(curdir)

class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands

class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)

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
    packages=['dinbrief', 'dinbrief.invoice', 'dinbrief.contrib'],
    #test_suite='dinbrief.tests',
    include_package_data=True,
    setup_requires=['django>=1.8,<1.9'],
    install_requires=read('requirements.txt').split('\n'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'build': build,
        'install_lib': install_lib,
        'compile_translations': compile_translations
    }
)
