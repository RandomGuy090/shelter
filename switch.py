import variables as var
import sys
from shelter import Shelter


class Switch():

	def switch(self, read):
		read = read.rsplit(" ")
		try:
			arg = read[1:]
			comm = read[0]
			firstLayer = list()
			for elem in arg: firstLayer.append(elem)
		except:
			firstLayer = None
			arg = None
			comm = read[0]
		# print(f"{comm} {arg}")
		# print(f"{self.data}")
		if comm in var.LS_KWORDS:			#eg ls
			return getattr(self, "case_LIST")()
		
		elif comm == "lol":					#eg lol
			return getattr(self, "case_LOL")()
		
		elif comm in var.EXT_KWORDS :		#eg exit
			return getattr(self, "case_EXIT")()

		elif comm in var.CD_KWORDS:			#eg cd sth
			if len(arg) > 0:				#if argumest exists
				if f"{comm} {arg[0]}" in var.CD_UP_KWORDS:	#eg cd ..
					return getattr(self, "case_CD_UP")()

				elif arg[0] in self.data: 	#eg cd path/to/file
					return getattr(self, "case_CD_to")(arg)

				elif arg[0].rsplit("/") in firstLayer: 	#eg cd path/to/file
					return getattr(self, "case_CD_to")(arg)

				elif f"{comm} {arg}" in var.CD_UP_KWORDS:	
					
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
				# return getattr(self, "case_go_to")(comm)	
				return getattr(self, "case_CD_to")(comm)	
				

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
		print("case_CD_UP")

		newPath = var.PATH.rsplit("']")
		newPath = newPath[:-2]
		tmp = ""
		for elem in newPath: 
			if not elem.startswith("['"): elem = f"['{elem}"
			if not elem.endswith("']"): elem = f"{elem}']"
			tmp+=elem
				

		if not tmp.endswith("']"): tmp += "']" 

		if tmp != "']":
			var.PATHDIR = eval(f'self.data{tmp}')
		else:
			self.case_CD()
			return

		var.PATH = ""
		for elem in tmp: var.PATH+=elem
		
		if not var.PATH.endswith("']") and len(var.PATH)>1: newPath += "']" 
		
		self.printOut()

	def case_CD_to(self, arg):
		if isinstance(arg, list): 	#if comes from cd {path}
			while[-1] == "":
				arg = arg[:-1]
			var.PATH = f"{var.PATH}{arg}"
		
		elif isinstance(arg, str): #if comes from only {path}
			var.PATH = f"{var.PATH}['{arg}']"

		var.PATHDIR = eval(f"self.data{var.PATH}")

		self.printOut()

	def case_go_to(self, loc):
		var.PATHDIR = var.PATHDIR[loc]	#go back
		var.PATH += f"{loc}/"
		self.printOut()

	def case_CD(self):
		var.PATHDIR = self.data
		var.PATH = ""
		self.printOut()
	

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




