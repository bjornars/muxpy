# -*- coding: utf-8 -*-
from distutils.core import setup
import re


def get_version():
    init_py = open('muxpy/__init__.py').read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
    return metadata['version']


setup(
    name='Muxpy',
    version=get_version(),
    author='Bjørnar Snoksrud',
    author_email='bjornar@snoksrud.no',
    packages=['muxpy'],
    scripts=['bin/muxpy'],
    license='ICS',
    description='A tmux session handler',
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    data_files=['README.rst'],
    url='https://github.com/bjornars/muxpy',
)
