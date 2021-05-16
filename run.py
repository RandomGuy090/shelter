#! /bin/python
import os, sys

from shelter import Shelter
from switch import  Cmd, Switch

import variables as var


if __name__ == "__main__":
	sh = Shelter()
	data = sh.decrypt(var.FILE)
	cmd = Cmd(data)
	var.PATHDIR = data
	
	cmd.printOut()
	while True:
		read = input(f"shelter> {var.PATH} >")
		cmd.switch(read)



