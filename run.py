#! /bin/python
import os, sys

from shelter import Shelter
from switch import Switch

FILE = "/home/randomguy90/PROGRAM/Python/shelter/passJson.txt"

EXT_KWORDS = ["q","exit","quit"]
LS_KWORDS = ["ls", "list"]

PATH = ""
PATHDIR = None


if __name__ == "__main__":
	sh = Shelter()
	data = sh.decrypt(FILE)
	PATHDIR = data
	while True:
		sh.list(PATHDIR)
		read = input(f"shelter> {PATH} >")
		read = read.rsplit(" ")

		if read[0] in EXT_KWORDS :
			sys.exit(0)

		else:

			if read == ['']:
				PATHDIR = data
				PATH = ""
				
			elif data[read[0]]:
				print(f"cd {read[0]}")
				try:
					PATHDIR = data[read[0]]
					PATH = read[0]
				except KeyError:
					print(f"shelter '{read[0]}' not found")
				
			#change pwd here


