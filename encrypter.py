# -*- coding: utf-8 -*-

import sys, atexit, signal, threading, handle_args, tools
from getpass import getpass
from os.path import getsize
from datetime import timedelta
from time import time, sleep


CHUNK_SIZE    =  20*2**10
CHUNK_N       =  0
VERBOSE       =  False
QUIET         =  False
INTER_MODE    =  False
RUNNING       =  False
ABORTED       =  False
PROC          =  None
STATUS        =  {"coded_bytes":0,"progress":"N/A","time_left":"N/A"}
data_in       =  sys.stdin
data_out      =  sys.stdout
msg_out       =  sys.stderr
start_time    =  None
end_time      =  None


# INTERNAL HANDLERS #


def _log(stuff, exit_status=None, pref="\r"):
	global RUNNING
	stuff = "MBencrypter: "+stuff
	stuff = stuff.split("\n")
	w = tools.console_size()[0]
	for i in xrange(len(stuff)):
		stuff[i] = stuff[i]+(" "*(w-len(stuff[i])))
	msg_out.write(pref+"\n".join(stuff)+"\n")
	msg_out.flush()
	if exit_status!=None:
		RUNNING = False
		sys.exit(exit_status)


def update_status(n=None,f=None):
	global STATUS
	if 'all_bytes' in STATUS:
		STATUS["progress"] = "{0:.0%}".format(STATUS['coded_bytes']/float(STATUS['all_bytes']))
		if start_time and STATUS['coded_bytes'] > 0:
			velocity = STATUS['coded_bytes']/(time()-start_time)
			bytes_left = STATUS['all_bytes']-STATUS['coded_bytes']
			STATUS["time_left"] = str(timedelta(seconds=bytes_left/velocity)).split(".")[0]
	if n:
		out = []
		for key in STATUS:
			out.append("{0}: {1}".format(key, STATUS[key]))
		_log("STATUS:\n"+"\n".join(out))


def show_progress():
	while RUNNING:
		update_status()
		msg_out.write(("\r" if not VERBOSE else "")+("MBencrypter:" if not INTER_MODE else ">>")+" PROGRESS: ")
		if "all_bytes" in STATUS:
			msg_out.write("{0:>5} -- Estimated time left: {1}".format(STATUS["progress"], STATUS["time_left"]))
		else:
			msg_out.write("N/A")
		msg_out.flush()
		sleep(0.5)


def _clean():
	data_in.close()
	data_out.close()

if hasattr(signal, "SIGUSR1"): signal.signal(signal.SIGUSR1, update_status)
atexit.register(_clean)


####################################################
def _encrypter(do_encrypt, inp, out, key, hex_mode):

	## INIZIALIZATION ##

	global data_in, data_out, start_time, end_time, STATUS, RUNNING, CHUNK_N

	if inp:
		try:
			data_in = open(inp,"rb")
			STATUS['all_bytes'] = (getsize(inp)/2) if hex_mode else getsize(inp)
		except IOError:
			_log("ERROR: can't open input file! Aborting.", 1)

	if out and (inp or out!=True):
		try:
			data_out = open((inp+".mbc" if do_encrypt else inp[:-4]) if out==True else out,"wb")
		except IOError:
			_log("ERROR: can't open output file! Aborting.", 1)

	if not key:
		while not key:
			key = getpass("Please type key:\n> ")

	start_time = time()
	RUNNING = True
	if PROC: PROC.start()

	## OCT KEY SETTING ##
	octKey = []
	for c in key:
		octKey += map(int, oct(ord(c))[1:])
	if len(octKey)%2: octKey.append(0)

	while True:

		try:
			chunk = data_in.read(CHUNK_SIZE)
			if VERBOSE: _log("debug: read chunk #{0} of {1} bytes. Bytes read = {2}".format(CHUNK_N, CHUNK_SIZE, len(chunk)))
			CHUNK_N += 1
			if not chunk:
				if VERBOSE: _log("\x07debug: breaking from while loop!")
				break

			if hex_mode and not do_encrypt:
				chunk += data_in.read(CHUNK_SIZE)
				LN = len(chunk)/2
				bytecode = (int(chunk[b:b+2],16) for b in xrange(0,len(chunk),2))
			else:
				LN = len(chunk)
				bytecode = (ord(byte) for byte in chunk)

		except IOError:
			_log("ERROR: error reading input file! Aborting.", 1)


		## BIN KEY SETTING ##
		binKey = []
		for c in xrange(len(key)):
			if (len(binKey) <= LN):
				binKey.append(ord(key[c]))
			else:
				binKey[c % LN] ^= ord(key[c])

		## ENCRYPTION PART ##
		coded = []
		for i in xrange(LN):

			try: coded.append(bytecode.next())
			except (ValueError, IndexError):
				_log("ERROR: The input data is not valid hex! Aborting.", 1)
			
			k = i%len(binKey)

			# XOR - if encoding
			if do_encrypt: coded[i] ^= binKey[k]

			# MISC
			rng = xrange(0, len(octKey), 2) if do_encrypt else xrange(-1, -len(octKey)-1, -2)
			s = 1 if do_encrypt else -1
			for j in rng:
				if bool(coded[i] & 2**octKey[j]) ^ bool(coded[i] & 2**octKey[j+1*s]):
					mask = 2**octKey[j] + 2**octKey[j+1*s]
					coded[i] ^= mask

			# XOR - if decoding
			if not do_encrypt: coded[i] ^= binKey[k]

			STATUS['coded_bytes'] += 1

		if VERBOSE: _log("debug: {0} bytes encoded. {1} bytes encoded until now.".format(len(coded), STATUS['coded_bytes']))

		## OUTPUT PART ##
		try:
			if hex_mode and do_encrypt:
				data_out.write(''.join(map("{0:02X}".format, coded)))
			else:
				data_out.write(''.join(map(chr,coded)))
			if VERBOSE: _log("debug: data successfully appended to output buffer.")
		except IOError:
			_log("ERROR: can't write to output file! Aborting.", 1)

	end_time = time()
	RUNNING = False
	if VERBOSE: _log("debug: completed! elapsed time: "+str(timedelta(seconds=time()-start_time)))


#####################################
def main(args_from_interactive=None):

	global VERBOSE, QUIET, STATUS, RUNNING, ABORTED, PROC

	try:
		args = handle_args.main(args_from_interactive)

		VERBOSE = args.v
		QUIET = args.q

		if not QUIET:
			PROC = threading.Thread(target=show_progress)

		if args.e:
			_encrypter(True, args.i, args.o, args.k, args.hex)
		elif args.d:
			_encrypter(False, args.i, args.o, args.k, args.hex)

		if not QUIET:
			msg_out.write(
				("\r" if not VERBOSE else "") +
				("MBencrypter:" if not INTER_MODE else ">>") +
				" PROGRESS: DONE! -- Execution time: " +
				str(timedelta(seconds=end_time-start_time)).split(".")[0] + "\n")
			msg_out.flush()


	except KeyboardInterrupt:
		RUNNING = False
		ABORTED = True
		if INTER_MODE: raise
		else: _log("Manually Interrupted!", 0, "\n")

if __name__ == "__main__": main()
