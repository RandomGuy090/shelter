#! /bin/python
import os, sys, readline, re
import atexit, getopt

from shelter import Shelter
from cmd import  Cmd
from autocomp import Completer

import variables as var


def show():
	"printouts elements from passed list"
	ls = cmd.printOut()[1]
	for elem in ls:
		print(elem)

def exit():
	"run as last, closes everything"
	var.LAST_READ = cmd.switch("cd")[0]
	sh.encrypt(var.PATHDIR, var.FILE)
	sh.delete_keys()

def printHelp():
	"help printout"
	print(""" ./shelter.py <options>
	   -f --file 		file location
	   -r --recipient	recipient       
	   -s --secret		import secret key
	   -p --public		import public key
			""")

def flags():
	try:
		argv = sys.argv[1:]
		options, reminder = getopt.getopt(argv,"f:r:h:s:p:",["file=","recip=", "help=", \
							"public=", "secret="])

		for opt, arg in options:
			if opt in ('-f', '--file'):
				var.FILE = arg
			elif opt in ('-r', '--recip'):
				var.RECIP_FLAG = arg
			elif opt in ("-s", "--secret"):
				var.PRIV_KEY = arg
			elif opt in ("-p", "--public"):
				var.PUBLIC_KEY = arg

			elif opt in ("-h", "--help"):
				printHelp()
				sys.exit(0)

	except getopt.GetoptError as e:
		print(e)
		printHelp()
		sys.exit(0)



if __name__ == "__main__":
	flags()
	sh = Shelter(var.FILE)
	cmd = Cmd()

	if var.PRIV_KEY:
		if sh.import_key(arg) != "ok":
			print("importing key error")
	if var.PUBLIC_KEY:
		if sh.import_key(arg) != "ok":
			print("importing key error")


	atexit.register(exit)

	while True:
		show()
		path = cmd.convToPath(var.PATH)
		prompt = cmd.promptColor("shelter>")
		
		if len(var.PATH) >1:
			read = input(f"{prompt}{path}>")
		else:
			read = input(f"{prompt}")
		
		cmd.switch(read)


