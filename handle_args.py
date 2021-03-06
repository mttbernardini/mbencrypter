# -*- coding: utf-8 -*-

# Copyright (c) 2015 Matteo Bernardini
# Copyright (c) 2015 Marco Bonelli
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

desc = """
| Symmetric Encryption Algorithm by Mattyw&MeBeiM |
---------------------------------------------------
This program will help you encrypting or decrypting
some data or a file using MB's algorithm.
You can also send a SIGUSR1 to this process to get
its progress status.
For a complete description please read the README file.

Note: if no parameter is specified the program will
run in interactive mode.
"""

def main(opt=None):

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=desc)

	action = parser.add_mutually_exclusive_group(required=True)
	action.add_argument('-e', action='store_true', help='run in encode mode.')
	action.add_argument('-d', action='store_true', help='run in decode mode.')

	parser.add_argument('-k', metavar='<string>', help='specify the key from a string. If no key is specified it will be asked via password prompt after the OEF of input data.')
	parser.add_argument('-i', metavar='<path>', help='specify the input file. Default to <stdin>.')
	parser.add_argument('-o', metavar='<path>', nargs='?', const=True, help='specify the output file. Leave empty to use the same path of the input file, adding/removing the .mbc extension. Default to <stdout>.')
	parser.add_argument('-hex', action='store_true', help='input/output data in base16.')
	parser.add_argument('-v', action='store_true', help='run in verbose mode.')
	parser.add_argument('-q', action='store_true', help='don\'t log progress status.')
	parser.add_argument('--version', action='version', version='MBencrypter 2.0')

	return parser.parse_args(opt)
