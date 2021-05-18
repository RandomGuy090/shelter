from shelter import Shelter
from switch import Switch
import variables as var

import pyperclip

class Cmd(Shelter, Switch):
	def __init__(self, data):
		self.data = data

	def printOut(self):
		data = var.PATHDIR
		for elem in data:	
			elem = self.checkType(elem, data)
			print(elem)

	def changeColor(self, txt, code:"[escCde, style, txtCol, bgcol]")-> "colored string":
		header = f"{code[0]}{code[1]};{code[2]};{code[3]}m"
		tail = "\033[0;0m"
		return f"{header}{txt}{tail}"
	
	def notFound(self, command, arg="not found"):
		header = f"\x1b[1;31m"
		tail = "\033[0;0m"
		print(f"{header} command : '{command}' {arg}{tail}")

	def convToPath(self, path):
		path = path[2:-2]
		path = path.replace("']['", "/")

		font = [ "1", "34", "49"]
		path = self.changeColor(path, ["\x1b[",font[0] ,font[1],font[2]])
		return path

	def promptColor(self, str):
		header = f"\x1b[1;32m"
		tail = "\033[0;0m"
		return f"{header}{str}{tail}"

	def clipboard(self, passwd):
		pyperclip.copy(passwd)
		self.copied()

	def copied(self):

		font = [ "1", "31", "49"]
		info = "--> password copied <--"
		info = self.changeColor(info, ["\x1b[",font[0] ,font[1],font[2]])
		print(info)

		
		