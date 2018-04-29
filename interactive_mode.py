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

import os, sys, threading, tempfile, encrypter, tools
from getpass import getpass
from time import sleep

_err1 = "Action not recognized!"
_p = "> "

def _checkFile(path):
	if not os.path.exists(path):
		return (False, "File not found!")
	elif not os.path.isfile(path):
		return (False, "The path you specified doesn't seem to be a file!")
	elif not os.access(path, os.R_OK):
		return (False, "You don't seem to have the permissions to read this file!")
	else:
		return (True, None)


def main():
	
	try:
		wd = tools.console_size()[0]
		print "\\{0:^{w}}/".format(" Symmetric Encryption Algorithm by Mattyw & MeBeiM ", w=wd-2)
		#print "\\\\"+"-"*(wd-4)+"//"
		print "\\\\{:_^{w}}//\n".format(" Version 2.0 ", w=wd-4)
		print "This tool will help you encoding/decoding data encrypted with the MB's Encryption Algorithm."
		print "Note: you can press [Ctrl+C] anytime to exit from this program."
	
		# Choose action
		while True:
			print "\nPlease choose if you need to:"
			print "1. Encode"
			print "2. Decode"
			action = raw_input(_p)
			if action in ["1","2"]: break
			else: print _err1
	
		w = "en" if action=="1" else "de"
	
		# Choose input
		while True:
			print "\nPlease choose if you need to "+w+"code a:"
			print "1. String of text / base16 data"
			print "2. File"
			type_inp = raw_input(_p)
			if type_inp in "12": break
			else: print _err1
	
		if type_inp == "2":
			while True:
				print "\nPlease specify the path of the file to be "+w+"coded (please use slashes as path delimiters, even if you are on Windows):"
				inp = raw_input(_p)
				c = _checkFile(inp)
				if c[0]: break
				else: print c[1]
		else:
			print "\nPlease type/paste the"+(" encoded" if w=="de" else '')+" data:"
			inp = raw_input(_p)
	
		# Choose output
		while True:
			print "\nPlease choose the output format:"
			print "1. Output as text / base16 data"
			print "2. Output as file on another path"
			if type_inp=="2": print "3. Output as file on the same folder"
			type_out = raw_input(_p)
			if type_out in ("123" if type_inp=="2" else "12"): break
			else: print _err1
	
		if type_out == "2":
			while True:
				print "\nPlease specify the path of the output file (please use slashes as path delimiters, even if you are on Windows):"
				out = raw_input(_p)
				c = _checkFile(out)
				if c[0]: break
				else: print c[1]
	
		# Read key
		while True:
			print "\nPlease type the key carefully, you'll be asked to confirm it."
			key = getpass(_p+'Key: ')
			if not key:
				print "A key is required!"
				continue
			if (key == getpass(_p+'Confirm key: ')): break
			else: print "The keys don't match. Try again."
	
		# Summary
		print "\n\n=== SUMMARY ==="
		print "Input data:"
		print inp
		print "\nOutput data:"
		if type_out=="1":
			print "<text>"
		elif type_out=="2":
			print out
		else:
			print inp+".mbc" if action=="1" else inp[:-4]
		print "\nKey:"
		print "*"*len(key)
		raw_input("\nPress [Enter] to start.")


		# Encrypter call
		args = ["-e" if action=="1" else "-d"]
		if type_inp=="1" and type_out=="1": args += ["-hex"]
		args += ["-k", key]
		if type_inp!="1":
			args += ["-i", inp]
		else:
			encrypter.data_in = tempfile.SpooledTemporaryFile()
			encrypter.data_in.write(inp)
			encrypter.STATUS['all_bytes'] = encrypter.data_in.tell() if action=="1" else encrypter.data_in.tell()/2
			encrypter.data_in.seek(0,0)
		if type_out!="1":
			args += ["-o"] + ([out] if type_out=="2" else [])
		else:
			encrypter.data_out = tempfile.SpooledTemporaryFile()

		encrypter.msg_out = sys.stdout		
		encrypter.INTER_MODE = True
		encrypter.main(args)
		
		if type_out=="1":
			print ">> Successfully "+w+"coded data:"
			encrypter.data_out.seek(0,0)
			print encrypter.data_out.read()
		else:
			print ">> "+w.title()+"coded data successfully written to file!"


		raw_input("\nProgram ended. Press [Enter] to exit.")
	

	except KeyboardInterrupt:
		raw_input("\nAborted. Press [Enter] to exit.")
	except SystemExit:
		raw_input("\nPress [Enter] to exit.")


if __name__ == "__main__": main()
