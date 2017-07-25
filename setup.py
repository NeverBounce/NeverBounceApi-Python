#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as fd:
    long_description = fd.read()

with open('LICENSE') as fd:
    license = fd.read()

setup(
    name='neverbounce-sdk',
    version='1.0.2',
    description="Python SDK for the NeverBounce API",
    long_description=long_description,
    author="NeverBounce Team",
    author_email='support@neverbounce.com',
    url='https://github.com/NeverBounce/NeverBounceApi-Python',
    packages=find_packages(include=['neverbounce_sdk']),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license=license,
    zip_safe=False,
    keywords='neverbounce',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
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
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=['pytest'],
)
