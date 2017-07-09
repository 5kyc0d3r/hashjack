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
import hashlib
from hashjack_tools import *
from datetime import datetime


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
  
Supported hash types: md5, sha-1, sha-256, sha-512

HashJack is a tool to easily crack password hashes using a dictionary / wordlist.
The project is licensed under the terms of the MIT license and is available as
FOSS (Free and Open Source Software) on Github. The latest version of this tool
can always be found at https://github.com/5kyc0d3r/hashjack.
'''.format(version, green + bold + project_site + white)


def start_cracking(hash_value, wordlist, verbose):
    hash_types = {'md5': 32, 'sha-1': 40, 'sha-256': 64, 'sha-512': 128}

    # If hash length is equal to 32, hash type is MD5
    if len(hash_value) == hash_types['md5']:
        hash_type = 'MD5'

    # If hash length is equal to 40, hash type is SHA-1
    elif len(hash_value) == hash_types['sha-1']:
        hash_type = 'SHA-1'

    # If hash length is equal to 64, hash type is SHA-256
    elif len(hash_value) == hash_types['sha-256']:
        hash_type = 'SHA-256'

    # If hash length is equal to 128, hash type is SHA-512
    elif len(hash_value) == hash_types['sha-512']:
        hash_type = 'SHA-512'

    # If the hash type could not be determined, throw an error and exit
    else:
        print(error('The specified hash is invalid or the type could not be determined.'))
        sys.exit(1)

    # Count the amount of words in the wordlist
    with open(wordlist) as f:
        print(info('Counting words from wordlist, this might take a while, please wait...'))
        word_count = sum(1 for _ in f)

    # If the -v or --verbose flag was set, print the info set by the user
    if verbose:
        print(info('Hash: ' + str(hash_value)))
        print(info('Hash type (auto-detected): ' + str(hash_type)))
        print(info('Wordlist path: ' + str(wordlist)))
        print(info('Word count: ' + str(word_count)))

    # Inform the user that HashJack is starting
    start_time = datetime.now()
    print('\n' + info('HashJack {} starting at {}'.format(version, start_time)))

    # Open the user specified wordlist
    with open(wordlist) as f:
        # Define a counter for keeping track of current word number
        c = 0

        # Read the wordlist file line by line
        for word in f:
            # Increase the word counter by 1 each time a new line is read
            c += 1

            # Strip new line characters from current wordlist word
            current_word = str(word).strip('\n')

            # If verbose output mode is enabled, print HashJack cracking status
            if verbose:
                if word_count % c == 0:
                    # Log the current cracking status of HashJack
                    print(log('Cracking hash ' + yellow + bold + str(hash_value) + white + green + ' with ' +
                              'word (%d/%d): ' % (c, word_count) + bold + blue + current_word + white))

            # If the hash type is MD5, use MD5 hashing function for cracking
            if hash_type == 'MD5':
                current_word_hash = hashlib.md5(current_word).hexdigest()

            # If the hash type is SHA-1, use SHA-1 hashing function for cracking
            elif hash_type == 'SHA-1':
                current_word_hash = hashlib.sha1(current_word).hexdigest()

            # If the hash type is SHA-256, use SHA-256 hashing function for cracking
            elif hash_type == 'SHA-256':
                current_word_hash = hashlib.sha256(current_word).hexdigest()

            # If the hash type is SHA-512, use SHA-512 hashing function for cracking
            elif hash_type == 'SHA-512':
                current_word_hash = hashlib.sha512(current_word).hexdigest()

            # If the hash type does not exist, throw an error and exit
            else:
                print(error('There is no function for this hash type.'))
                sys.exit(1)

            # If a password match was found, stop the cracking process and show the hash value to the user
            if hash_value == current_word_hash:
                # Current time
                stop_time = datetime.now()

                # The total time taken to crack the hash
                total_time = stop_time - start_time

                print('')
                print(success(green + bold + 'Password hash match found at {}.'.format(datetime.now()) + white))
                print(success(green + bold + 'Total running time (H:M:S:MS): {}.'.format(total_time) + white))
                print(success(green + bold + 'Hash: {} => Value: {}\n'.format(hash_value, current_word) + white))
                sys.exit(0)
            else:
                # If no hash match was found, try the next available word in dictionary / wordlist
                continue

        # No password hash match found
        stop_time = datetime.now()
        total_time = stop_time - start_time
        print('')
        print(success(green + bold + 'Finished at: {}.'.format(stop_time) + white))
        print(success(green + bold + 'Total running time (H:M:S:MS): {}.'.format(total_time) + white))
        print(error(red + bold + 'Password hash could not be found.\n' + white))
        sys.exit(1)


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

    # Call the start_cracking function to start the cracking process
    start_cracking(hash_value, wordlist, verbose)


if __name__ == "__main__":
    main()
