#!/usr/bin/python

import os
import shutil
from setuptools import setup

if not os.path.exists('scripts'):
    os.makedirs('scripts')

try:
    shutil.copyfile('hashjack.py', 'scripts/hashjack')
except IOError:
    print("Could not copy hashjack.py file. You can ignore this if you're installing with pip.")

setup(
    name='hashjack',
    version='1.0.3',
    packages=['hashjack_tools'],
    scripts=['scripts/hashjack'],
    url='https://github.com/5kyc0d3r/hashjack',
    download_url='https://github.com/5kyc0d3r/hashjack/archive/1.0.2.tar.gz',
    keywords=['hashjack', 'hashing', 'cracking', 'brute-force', 'python'],
    license='MIT',
    author='5kyc0d3r',
    author_email='skycoder.official@protonmail.com',
    description='Open source tool for cracking password hashes.'
)
