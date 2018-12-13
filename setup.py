#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path
from re import search, M

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return open(path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='neverbounce-sdk',
    version=find_version('neverbounce_sdk/__init__.py'),
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=['pytest'],
)
