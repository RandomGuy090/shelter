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

if __name__ == "__main__":

	cmd = Cmd()

	while True:
		show()
		path = cmd.convToPath(var.PATH)
		prompt = cmd.promptColor("shelter>")
		
		if len(var.PATH) >1:
			read = input(f"{prompt}{path}>")
		else:
			read = input(f"{prompt}")
		
		cmd.switch(read)


