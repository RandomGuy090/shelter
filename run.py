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

def printHelp():
	"help printout"
	print(""" ./shelter.py <options>
		

		""")
def flags():
	try:
		argv = sys.argv[1:]
		options, reminder = getopt.getopt(argv,"f:r:h:",["file=","recip=", "help="])

		for opt, arg in options:
		    if opt in ('-f', '--file'):
		        var.FILE = arg
		    elif opt in ('-r', '--recip'):
		        var.RECIP_FLAG = arg
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


