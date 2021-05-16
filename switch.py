import variables as var
import sys
from shelter import Shelter


class Switch():

	def switch(self, read):
		read = read.rsplit(" ")
		try:
			arg = read[1:]
			comm = read[0]
		except:
			arg = None
			comm = read[0]
		
		if comm in var.LS_KWORDS:			#eg ls
			return getattr(self, "case_LIST")()
		
		elif comm == "lol":					#eg lol
			return getattr(self, "case_LOL")()
		
		elif comm in var.EXT_KWORDS :		#eg exit
			return getattr(self, "case_EXIT")()

		elif comm in var.CD_KWORDS:			#eg cd sth
			if arg != None:				#if argumest exists
				if f"{comm} {arg[0]}" in var.CD_UP_KWORDS:	#eg cd ..
					return getattr(self, "case_CD_UP")()

				elif arg[0] in self.data:
					print("goto")
					return getattr(self, "case_CD_to")(arg)
				elif f"{comm} {arg}" in var.CD_UP_KWORDS:	#eg cd path/to/file
					return getattr(self, "case_CD_UP")()
				else:					#just cd to root
					return getattr(self, "case_CD")()

			else:
				return getattr(self, "case_CD")()
		elif comm in var.PATHDIR:		#eg name of shelter
			if isinstance(var.PATHDIR[comm], str):	#if it is string
				passwd = var.PATHDIR[comm]	#this is tem, default paste to clipboard
				print(f"password {passwd}")		#tmp
				return None
			else:
				return getattr(self, "case_go_to")(comm)	

		elif comm == "":
			return getattr(self, "case_CD")()
		else:
			return getattr(self, "case_NONE")(comm)
	

	def case_LIST(self):
		self.printOut()

	def case_LOL(self):
		print("LOOOOL")
		self.printOut()
	
	def case_EXIT(self):
		sys.exit(0)

	def case_CD_UP(self):
		newPath = var.PATH.rsplit("/")[:-2]
		tmp = str(newPath).replace(", ", "][")
		if tmp != "[]":
			var.PATHDIR = eval(f'self.data{tmp}')
		else:
			var.PATHDIR = eval(f'self.data')

		var.PATH = ""
		for elem in newPath: var.PATH+=elem+"/"
		self.printOut()

	def case_CD_to(self, arg):
		tmp = ""
		for elem in arg:
			tmp += f"['{elem}']"
		print(tmp)
		var.PATH = tmp.replace("']", "/").replace("['","/")
		if var.PATH.startswith("/"): var.PATH = var.PATH[1:] 
		print(var.PATH)
		var.PATHDIR = eval(f'self.data{tmp}')
	


	def case_CD(self):
		var.PATHDIR = self.data
		var.PATH = ""
		self.printOut()
	
	def case_go_to(self, loc):
		var.PATHDIR = var.PATHDIR[loc]	#go back
		var.PATH += f"{loc}/"

	def case_NONE(self, comm):
		print(f"shelter '{comm}' not found")	#if not found


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




