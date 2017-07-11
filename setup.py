#!/usr/bin/python

import os
import shutil
from setuptools import setup

hash_jack_version = '1.0.4'

if not os.path.exists('scripts'):
    os.makedirs('scripts')

try:
    shutil.copyfile('hashjack.py', 'scripts/hashjack')
except IOError:
    print("Could not copy hashjack.py file. You can ignore this if you're installing with pip.")

setup(
    name='hashjack',
    version=hash_jack_version,
    packages=['hashjack_tools'],
    scripts=['scripts/hashjack'],
    url='https://github.com/5kyc0d3r/hashjack',
    download_url='https://github.com/5kyc0d3r/hashjack/archive/{}.tar.gz'.format(hash_jack_version),
    keywords=['hashjack', 'hashing', 'cracking', 'brute-force', 'python'],
    license='MIT',
    author='5kyc0d3r',
    author_email='skycoder.official@protonmail.com',
    description='Open source tool for cracking password hashes.'
)
