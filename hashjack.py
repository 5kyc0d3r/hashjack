#!/usr/bin/python

"""
MIT License

Copyright (c) 2017 5kyc0d3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import required modules
import os
import sys
import getopt
from hashjack_tools import *


# Script version number variable
version = '1.0.1'

# HashJack project site variable
project_site = 'https://github.com/5kyc0d3r/hashjack'

# Script help menu variable
usage = '''
HashJack {} - (C) 2017 5kyc0d3r
View this project on Github: {}

usage: ./hashjack.py --hash <hash-to-crack> --wordlist <path-to-wordlist> [options]

Required:

  -H, --hash <hash-to-crack>            specify the hash to crack (hash type auto-detected)
  -w, --wordlist <path-to-wordlist>     specify the path to the wordlist file

Options:

  -h, --help                            print this help menu and exit
  -V, --version                         print the hashjack version number and exit
  -v, --verbose                         enable verbose output mode
'''.format(version, green + bold + project_site + white)


def start_cracking(hash_value, wordlist, verbose):
    if verbose:
        print(info('Hash: ' + str(hash_value)))
        print(info('Wordlist path: ' + str(wordlist)))


def main(hash_value=None, wordlist=None, verbose=False):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hVvH:w:', ['help', 'version', 'verbose', 'hash=', 'wordlist='])
    except getopt.GetoptError as e:
        print(usage)
        print(str(e) + '\n')
        sys.exit(1)

    for opt, arg in opts:

        if opt in ('-h', '--help'):
            print(usage)
            sys.exit(0)

        elif opt in ('-V', '--version'):
            print('HashJack version %s' % version)
            sys.exit(0)

        elif opt in ('-v', '--verbose'):
            verbose = True

        elif opt in ('-H', '--hash'):
            hash_value = arg

        elif opt in ('-w', '--wordlist'):
            wordlist = arg

    # Check if hash and wordlist value is empty
    if not hash_value or not wordlist:
        print(usage)
        sys.exit(1)

    # Check if wordlist exists
    if os.path.isfile(wordlist):
        pass
    else:
        print(error('The specified wordlist is not a file or does not exist.'))
        sys.exit(1)

    start_cracking(hash_value, wordlist, verbose)


if __name__ == "__main__":
    main()
