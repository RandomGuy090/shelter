#! /bin/python
import os, sys

from shelter import Shelter
from switch import Switch

FILE = "/home/randomguy90/PROGRAM/Python/shelter/passJson.txt"

EXT_KWORDS = ["q","exit","quit"]
LS_KWORDS = ["ls", "list"]
CD_KWORDS = ["", "cd", ]
CD_UP_KWORDS = ["cd .."]


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
			print(f"PATH::: {PATH}")
			if read[0] in CD_KWORDS:
				if len(read) >1:
					if f"{read[0]} {read[1]}" in CD_UP_KWORDS:
						print(PATHDIR)
						print("goup")

						# tmp = PATH.replace("/", '"]["')[:-4]
						newPath = PATH.rsplit("/")[:-2]
						tmp = str(newPath).replace(", ", "][")
						print(tmp)
						print(tmp)

						print(PATHDIR)
						print(f"PATHDIR{tmp}")
						PATHDIR = eval(f'data{tmp}')
						PATH = ""
						for elem in newPath: PATH+=elem+"/"
						print(PATH)
					if read[0] == "cd":
						
						pass
				else:
					PATHDIR = data
					PATH = ""
			elif read[0] in PATHDIR:

				if isinstance(PATHDIR[read[0]], str):
					passwd = PATHDIR[read[0]]
					print(f"password {passwd}")
				else:
					PATHDIR = PATHDIR[read[0]]
					PATH += f"{read[0]}/"

			else:
				print(f"shelter '{read[0]}' not found")
				
			#change pwd here


