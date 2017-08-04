#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path
from neverbounce_sdk import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='neverbounce-sdk',
    version=__version__,
    description="Official Python SDK for the NeverBounce API",
    long_description=long_description,
    author="NeverBounce Team",
    author_email='support@neverbounce.com',
    url='https://github.com/NeverBounce/NeverBounceApi-Python',
    packages=find_packages(include=['neverbounce_sdk']),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license='MIT',
    zip_safe=False,
    keywords=['neverbounce', 'api', 'email', 'verification', 'cleaning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=['pytest'],
)
