#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


setup(
    name='vpnmenu',
    version='0.1.0',
    license='BSD',
    description='Connect to your VPNs defined in NetworkManager using dynamic menus',
    long_description='Connect to your VPNs defined in NetworkManager using dynamic menus',
    author='Idaho Frost',
    author_email='frostidaho@gmail.com',
    url='https://github.com/frostidaho/python-vpnmenu',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        'python-networkmanager',
        'dynmen>=0.1.0',
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'vpnmenu = vpnmenu.cli:main',
        ]
    },
)
