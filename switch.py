import variables as var
import sys
from re import sub

class Switch():

	def switch(self, read:str):
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

		if comm in var.LS_KWORDS:			
			"eg ls"
			return getattr(self, "case_LIST")()
		
		elif comm == "lol":					
			"eg lol"
			return getattr(self, "case_LOL")()
		
		elif comm in var.EXT_KWORDS :		
			"eg exit"
			return getattr(self, "case_EXIT")()

		elif comm in var.CD_KWORDS:		
			"eg cd sth"	
			if len(arg) > 0:				#if argumest exists
				if f"{comm} {arg[0]}" in var.CD_UP_KWORDS:	
					"eg cd .."
					return getattr(self, "case_CD_UP")()

				elif arg[0] in self.data: 	
					"eg cd path/to/file"
					return getattr(self, "case_CD_to")(arg)

				elif arg[0].rsplit("/") in firstLayer: 	
					"eg cd path/to/file"
					return getattr(self, "case_CD_to")(arg)

				elif f"{comm} {arg}" in var.CD_UP_KWORDS:	
					"eg cd .."
					return getattr(self, "case_CD_UP")()
				
				else:					
					"just cd to root"
					return getattr(self, "case_CD")()

			else:
				return getattr(self, "case_CD")()
		elif comm in var.PATHDIR:		#eg name of shelter
			if isinstance(var.PATHDIR[comm], str):	#if it is string
				passwd = var.PATHDIR[comm]	#this is tem, default paste to clipboard
				self.clipboard(passwd)		#tmp
				return None
			else:
				return getattr(self, "case_CD_to")(comm)	
				
		elif comm == "":
			return getattr(self, "case_CD")()
		elif comm in "reset":
			return getattr(self, "case_RESET")()

		elif comm in var.NEW_SHELTER_KWORDS:		#eg add XX
			return getattr(self, "case_CREATE_DIR")(arg)

		elif comm in var.NEW_FILES_KWORDS:		#eg add XX
			return getattr(self, "case_CREATE_FILE")(arg)

		elif comm in var.DEL_KWORDS:		#eg add XX
			return getattr(self, "case_DELETE")(arg)

		#--- adding new cases here
		else:
			return getattr(self, "case_NONE")(comm)
	

	def case_LIST(self):
		"eg ls"
		self.printOut()

	def case_LOL(self):
		"eg testing"
		print("LOOOOL")
		self.printOut()
	
	def case_EXIT(self):
		"eg q"
		sys.exit(0)

	def case_CD_UP(self):
		"eg cd .."

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

	def case_CD_to(self, arg:str):
		"if comes from cd PATH"
		if isinstance(arg, list): 	
			while[-1] == "":
				arg = arg[:-1]
			var.PATH = f"{var.PATH}{arg}"
		
		elif isinstance(arg, str): #if comes from only {path}
			var.PATH = f"{var.PATH}['{arg}']"

		var.PATHDIR = eval(f"self.data{var.PATH}")

		self.printOut()

	def case_go_to(self, loc:str):
		var.PATHDIR = var.PATHDIR[loc]	#go back
		var.PATH += f"{loc}/"
		self.printOut()

	def case_CD(self):
		"eg. cd"
		var.PATHDIR = self.data
		var.PATH = ""
		ret = self.printOut()
		return ret

	def case_NONE(self, comm:str):
		"eg.    "
		self.notFound(comm)	#if not found

	def case_RESET(self):
		"eg reset"
		print(chr(27) + "[2J")

	def case_CREATE_DIR(self, arg:str, command="create"):
		"create"
		if len(arg) == 0 :
			return self.notFound(command, "no argument") 
		for elem in arg:
			if " " in elem: continue 
			elif len(elem) == 0: continue 
			var.PATHDIR[elem] = dict()
		self.printOut()


	def case_CREATE_FILE(self, arg:str, command="add"):
		"eg add"
		if len(arg) == 0 :
			return self.notFound(command, "no argument") 

		out = []
		for elem in arg:
			if len(elem) > 0 and  not " " in elem:
				out.append(elem)
		arg = out		
		
		if len(arg)%2:
			self.notFound({arg[-1]}, " has no content" )
		
		for i in range(0, (len(arg)-1), 2 ):
			name = arg[i]
			content = arg[i+1]
			if " " in name or " " in content: continue 
			elif len(name) == 0 or len(content) == 0: continue 
			
			var.PATHDIR[name] = content
		
		self.printOut()

	def case_DELETE(self, arg:str):
		"eg rm"
		for elem in arg:
			del var.PATHDIR[elem]
		self.printOut()
	


	

