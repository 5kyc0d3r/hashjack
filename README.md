## HashJack
[![Build Status](https://travis-ci.org/5kyc0d3r/hashjack.svg?branch=master)](https://travis-ci.org/5kyc0d3r/hashjack) [![Packagist](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org) [![Packagist](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/5kyc0d3r/hashjack/blob/master/LICENSE) [![Packagist](https://img.shields.io/badge/OS-linux-blue.svg)](https://www.linux.com)

![alt text](http://i.imgur.com/j4XFn3V.png "HashJack v1.0.4")


Open source tool for cracking hashes built in Python.

## Usage
```
HashJack 1.0.4 - (C) 2017 5kyc0d3r
View this project on Github: https://github.com/5kyc0d3r/hashjack

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
  -s, --hashes                          print all the supported hash algorithms and exit

Supported hash types:

  Auto detected
  =============
  md5, sha-1, sha-224, sha-256, sha-384, sha-512, mysql-4.1+

  Not auto detected
  =================
  The following hash algorithms are not auto-detected by HashJack. You will have to
  manually specify the type with the -t, --type <hash-type> flag for these.

  LM, NTLM

Total hashing algorithms implemented: 9

HashJack is a tool to easily crack password hashes using a dictionary / wordlist.
The project is licensed under the terms of the MIT license and is available as
FOSS (Free and Open Source Software) on Github. The latest version of this tool
can always be found at https://github.com/5kyc0d3r/hashjack.
```


## Installation
### Pip
Hashjack is available on PyPi and can therefore be installed with pip.

1. `$ sudo pip install hashjack`

2. Run hashjack:

    `$ hashjack`

> To upgrade using pip, run the same command as above with the `--upgrade` flag.
>
> Example: `$ sudo pip install hashjack --upgrade`


### Install from source
1. Clone the git repository

    `$ git clone https://github.com/5kyc0d3r/hashjack.git`

2. Go into the newly cloned repository directory

    `$ cd hashjack`

3. Run the setup.py

    `$ sudo python setup.py install`

4. Run hashjack

    `$ hashjack`


## License
This software is licensed under the terms of the MIT License.
