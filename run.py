#! /bin/python
import os, sys, readline, re

from shelter import Shelter
from cmd import  Cmd
from autocomp import Completer

import variables as var


if __name__ == "__main__":
	sh = Shelter()
	data = sh.decrypt(var.FILE)
	cmd = Cmd(data)
	
	var.PATHDIR = data
	cmd.printOut()

	while True:
		path = cmd.convToPath(var.PATH)
		prompt = cmd.promptColor("shelter>")
		if len(var.PATH) >1:
			read = input(f"{prompt}{path}>")
		else:
			read = input(f"{prompt}")
		cmd.switch(read)