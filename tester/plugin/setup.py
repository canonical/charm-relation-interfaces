#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-interface-tester',
    version='0.1.0',
    author='Pietro Pasotti',
    author_email='pietro.pasotti@canonical.com',
    maintainer='Pietro Pasotti',
    maintainer_email='pietro.pasotti@canonical.com',
    license='GNU GPL v3.0',
    url='https://github.com/PietroPasotti/pytest-interface-tester',
    description='Pytest plugin to test charm relation interfaces.',
    long_description=read('README.md'),
    py_modules=['pytest_interface_tester'],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=3.5.0',
        # "scenario"  # it needs ops-scenario, but that's not on pip. install it manually.
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'interface-tester = pytest_interface_tester',
        ],
    },
)
