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
from passlib.hash import lmhash
from passlib.hash import nthash
from passlib.hash import mysql41
from passlib.exc import PasswordSizeError


# Script version number variable
version = '1.0.3'

# HashJack project site variable
project_site = 'https://github.com/5kyc0d3r/hashjack'

# Supported hash types
supported_hashes = ['md5', 'sha-1', 'sha-224', 'sha-256', 'sha-384', 'sha-512', 'mysql-41', 'lm', 'ntlm']

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
  -t, --type <hash-type>                manually specify the type of the hash
  -r, --restore <restore-file>          use a hashjack restore file to continue hash cracking from a previous session
  
Supported hash types:

  Auto detected
  =============
  md5, sha-1, sha-224, sha-256, sha-384, sha-512, mysql-4.1+

  Not auto detected
  =================
  The following hash algorithms are not auto-detected by HashJack. You will have to
  manually specify the type with the -t, --type <hash-type> flag for these.

  LM, NTLM
    
Total hashing algorithms implemented: {}

HashJack is a tool to easily crack password hashes using a dictionary / wordlist.
The project is licensed under the terms of the MIT license and is available as
FOSS (Free and Open Source Software) on Github. The latest version of this tool
can always be found at https://github.com/5kyc0d3r/hashjack.
'''.format(version, green + bold + project_site + white, len(supported_hashes))


def check_hash(hash_value):
    hash_types = {'md5': 32, 'sha-1': 40, 'sha-224': 56, 'sha-256': 64, 'sha-384': 96, 'sha-512': 128, 'mysql41': 41}

    # If hash length is equal to 32, hash type is MD5
    if len(hash_value) == hash_types['md5']:
        return 'MD5'

    # If hash length is equal to 40, hash type is SHA-1
    elif hash_value.islower() and len(hash_value) == hash_types['sha-1']:
        return 'SHA-1'

    # If hash length is equal to 56, hash type is SHA-224
    elif hash_value.islower() and len(hash_value) == hash_types['sha-224']:
        return 'SHA-224'

    # If hash length is equal to 64, hash type is SHA-256
    elif hash_value.islower() and len(hash_value) == hash_types['sha-256']:
        return 'SHA-256'

    # If hash length is equal to 96, hash type is SHA-384
    elif hash_value.islower() and len(hash_value) == hash_types['sha-384']:
        return 'SHA-384'

    # If hash length is equal to 128, hash type is SHA-512
    elif hash_value.islower() and len(hash_value) == hash_types['sha-512']:
        return 'SHA-512'

    # If hash begins with '*' and length is equal to 41, hash type is MySQL 4.1+
    elif hash_value[0] == '*' and hash_value.isupper() and len(hash_value) == hash_types['mysql41']:
        return 'MYSQL-41'

    # If the hash type could not be determined, throw an error and exit
    else:
        print(error('The specified hash is invalid or the type could not be determined.'))
        sys.exit(1)


def start_cracking(hash_value, wordlist, hash_type, verbose, start_from_line=1):
    # Define a counter for keeping track of current word number
    c = 0

    try:
        # Check if required to start cracking from a specific line in wordlist
        if start_from_line == 1:
            pass
        else:
            print(info('Restoring from a previous cracking session...'))

        # Check if the hash provided is valid
        if hash_type == '':
            hash_type = check_hash(hash_value)
            auto_detected = True
        else:
            hash_type = hash_type.upper()
            auto_detected = False

        # Count the amount of words in the wordlist
        with open(wordlist) as f:
            print(info('Counting words from wordlist, this might take a while, please wait...'))
            word_count = sum(1 for _ in f)

        # If the -v or --verbose flag was set, print the info set by the user
        if verbose:
            print(info('Hash: ' + str(hash_value)))

            if auto_detected:
                print(info('Hash type (auto-detected): ' + str(hash_type)))
            else:
                print(info('Hash type (user-specified): ' + str(hash_type)))

            print(info('Wordlist path: ' + str(wordlist)))
            print(info('Word count: ' + str(word_count)))

        hash_cracked = False
        current_word = ''

        # Inform the user that HashJack is starting
        start_time = datetime.now()
        print('\n' + info('HashJack {} starting at {}'.format(version, start_time)))

        # Open the user specified wordlist
        with open(wordlist, 'rb') as f:
            restored_from_line = False
            # Read the wordlist file line by line
            for i, word in enumerate(f):
                # Increase the word counter by 1 each time a new line is read
                c += 1

                if i + 1 == start_from_line:
                    restored_from_line = True

                if not restored_from_line:
                    continue

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

                # If the hash type is SHA-224, use SHA-224 hashing function for cracking
                elif hash_type == 'SHA-224':
                    current_word_hash = hashlib.sha224(current_word).hexdigest()

                # If the hash type is SHA-256, use SHA-256 hashing function for cracking
                elif hash_type == 'SHA-256':
                    current_word_hash = hashlib.sha256(current_word).hexdigest()

                # If the hash type is SHA-384, use SHA-384 hashing function for cracking
                elif hash_type == 'SHA-384':
                    current_word_hash = hashlib.sha384(current_word).hexdigest()

                # If the hash type is SHA-512, use SHA-512 hashing function for cracking
                elif hash_type == 'SHA-512':
                    current_word_hash = hashlib.sha512(current_word).hexdigest()

                # If the hash type is MYSQL-41, use MYSQL-41 hashing function for cracking
                elif hash_type == 'MYSQL-41':
                    try:
                        current_word_hash = mysql41.hash(current_word)
                    except PasswordSizeError:
                        print(info('The password "{}" in the wordlist is too long for a MySQL 4.1+ hash. '
                                   'Skipping this one...'.format(current_word)))
                        continue

                # If the hash type is LM, use LM hashing function for cracking
                elif hash_type == 'LM':
                    try:
                        if lmhash.verify(current_word, hash_value):
                            hash_cracked = True
                            break
                        else:
                            continue
                    except ValueError:
                        print(error('The specified hash is not a valid LM hash (must be exactly 32 chars long).'))
                        sys.exit(1)

                # If the hash type is NTLM, use NTLM hashing function for cracking
                elif hash_type == 'NTLM':
                    try:
                        if nthash.verify(current_word, hash_value):
                            hash_cracked = True
                            break
                        else:
                            continue

                    except PasswordSizeError:
                        print(info('The password "{}" in the wordlist is too long for a NTLM hash. '
                                   'Skipping this one...'.format(current_word)))
                        continue

                    except ValueError:
                        print(error('The specified hash is not a valid NTLM hash (must be exactly 32 chars long).'))
                        sys.exit(1)

                # If the hash type does not exist, throw an error and exit
                else:
                    print(error('There is no function for this hash type.'))
                    sys.exit(1)

                # If a password match was found, stop the cracking process and show the hash value to the user
                if hash_value.lower() == current_word_hash.lower():
                    hash_cracked = True
                    break
                else:
                    # If no hash match was found, try the next available word in dictionary / wordlist
                    continue

            # If a password hash match was found
            if hash_cracked:
                print('')
                hash_found(start_time, hash_value, current_word)
                sys.exit(0)

            # If no password hash match was found
            else:
                print('')
                hash_not_found(start_time)
                sys.exit(1)

    except KeyboardInterrupt:
        print('\n' + info('Operation cancelled by User. HashJack shutting down...'))
        print(info('Writing a HashJack restore file...'))

        restore_filename = 'hashjack'
        extension = '.restore'

        while True:
            current_time = str(datetime.now())
            restore_filename = (restore_filename + '-' + current_time + extension).replace(' ', '-')

            # If a file with the restore_filename name does not exist, create it
            if not os.path.isfile(restore_filename):
                with open(restore_filename, 'wb') as f:
                    f.write(str(dict(hash_value=hash_value, wordlist=wordlist, line=c, hash_type=hash_type)) + '\n')
                    break

            # If the restore file exists, generate a new name and write it
            else:
                print(error('Failed to create restore file. File "{}" already exists. Trying again...'
                            .format(restore_filename)))
                continue

        print(success('Restore file written to "{}".\n'.format(restore_filename)))
        sys.exit(0)


def main(hash_value=None, wordlist=None, hash_type='', restore_file='', verbose=False):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hVvH:w:t:r:', ['help', 'version', 'verbose', 'hash=', 'wordlist=',
                                                                 'type=', 'restore='])
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

        elif opt in ('-t', '--type'):
            hash_type = arg

        elif opt in ('-r', '--restore'):
            restore_file = arg

    # Line number in wordlist to start reading from
    line = 1

    # Check if a restore file was used to continue a previous cracking session
    if restore_file == '':
        pass
    else:
        try:
            with open(restore_file, 'rb') as rf:
                try:
                    restore_file = eval(rf.read())
                    hash_value = restore_file['hash_value']
                    line = restore_file['line']
                    wordlist = restore_file['wordlist']
                    hash_type = restore_file['hash_type']
                except SyntaxError:
                    print(error('A syntax error occurred while reading "{}".'.format(restore_file)))
                    sys.exit(1)

                except KeyError:
                    print(error('A key error occurred while reading "{}". This could be due to a badly coded restore '
                                'file.'.format(restore_file)))
                    sys.exit(1)

        except IOError:
            print(error('The restore file "{}" does not exist or is not a file.'.format(restore_file)))
            sys.exit(1)

    # Check if hash and wordlist value is empty
    if not hash_value or not wordlist:
        print(usage)
        sys.exit(1)

    # Check if the hash type is valid
    if hash_type == '' or hash_type.lower() in supported_hashes:
        pass
    else:
        print(error('The specified hash type is not supported.'))
        print('Supported hash types: {}'.format(', '.join(supported_hashes)))
        sys.exit(1)

    # Check if wordlist exists
    if os.path.isfile(wordlist):
        pass
    else:
        print(error('The specified wordlist is not a file or does not exist.'))
        sys.exit(1)

    # Call the start_cracking function to start the cracking process
    start_cracking(hash_value, wordlist, hash_type, verbose, start_from_line=line)


if __name__ == "__main__":
    main()
