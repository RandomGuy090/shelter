#! /bin/python
import os, sys, readline, re
import atexit

from shelter import Shelter
from cmd import  Cmd
from autocomp import Completer

import variables as var


def show():
	ls = cmd.printOut()[1]
	for elem in ls:
		print(elem)

if __name__ == "__main__":
	sh = Shelter(var.FILE)
	cmd = Cmd()


	def exit():
		var.LAST_READ = cmd.switch("cd")[0]

		sh.encrypt(var.PATHDIR, var.FILE)

		
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


