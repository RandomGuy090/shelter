import variables as var
import sys
from re import sub

class Switch(object):

	def switch(self, read:str):
		read = read.rsplit(" ")
		try:
			arg = read[1:]
			comm = read[0]
			first_layer = list()
			for elem in arg: first_layer.append(elem)
		except:
			first_layer = None
			arg = None
			comm = read[0]

		if comm in var.LS_KWORDS:			
			"eg ls"
			return getattr(self, "case_list")()
		
		elif comm == "lol":					
			"eg lol"
			return getattr(self, "case_lol")()
		
		elif comm in var.EXT_KWORDS :		
			"eg exit"
			return getattr(self, "case_exit")()

		elif comm in var.CD_KWORDS:		
			"eg cd sth"	
			if len(arg) > 0:				#if argumest exists
				if f"{comm} {arg[0]}" in var.CD_UP_KWORDS:	
					"eg cd .."
					return getattr(self, "case_cd_up")()

				elif arg[0] in self.data: 	
					"eg cd path/to/file"
					return getattr(self, "case_cd_to")(arg)

				elif arg[0].rsplit("/") in first_layer: 	
					"eg cd path/to/file"
					return getattr(self, "case_cd_to")(arg)

				elif f"{comm} {arg}" in var.CD_UP_KWORDS:	
					"eg cd .."
					return getattr(self, "case_cd_up")()
				
				else:					
					"just cd to root"
					return getattr(self, "case_cd")()

			else:
				return getattr(self, "case_cd")()
		elif comm in var.PATHDIR:		#eg name of shelter
			if isinstance(var.PATHDIR[comm], str):	#if it is string
				passwd = var.PATHDIR[comm]	#this is tem, default paste to clipboard
				self.clipboard(passwd)		#tmp
				return None
			else:
				return getattr(self, "case_cd_to")(comm)	
				
		elif comm == "":
			return getattr(self, "case_cd")()
		elif comm in "reset":
			return getattr(self, "case_reset")()

		elif comm in var.NEW_SHELTER_KWORDS:		#eg add _xx
			return getattr(self, "case_create_dir")(arg)

		elif comm in var.NEW_FILES_KWORDS:		#eg add _xx
			return getattr(self, "case_create_file")(arg)

		elif comm in var.DEL_KWORDS:		#eg add _xx
			return getattr(self, "case_delete")(arg)

		elif comm in var.GEN_WORDS:		#eg generate _xx
			return getattr(self, "case_generate")(arg)

		#--- adding new cases here
		else:
			return getattr(self, "caseNone")(comm)
	

	def case_list(self):
		"eg ls"
		self.print_out()

	def case_lol(self):
		"eg testing"
		print("_looool")
		self.print_out()
	
	def case_exit(self):
		"eg q"
		sys.exit(0)

	def case_cd_up(self):
		"eg cd .."

		new_path = var.PATH.rsplit("']")
		new_path = new_path[:-2]
		tmp = ""
		for elem in new_path: 
			if not elem.startswith("['"): elem = f"['{elem}"
			if not elem.endswith("']"): elem = f"{elem}']"
			tmp+=elem
				
		if not tmp.endswith("']"): tmp += "']" 

		if tmp != "']":
			var.PATHDIR = eval(f'self.data{tmp}')
		else:
			self.case_cd()
			return

		var.PATH = ""
		for elem in tmp: var.PATH+=elem
		
		if not var.PATH.endswith("']") and len(var.PATH)>1: new_path += "']" 
		
		self.print_out()

	def case_cd_to(self, arg:str):
		"if comes from cd _path"
		if isinstance(arg, list): 	
			while[-1] == "":
				arg = arg[:-1]
			var.PATH = f"{var.PATH}{arg}"
		
		elif isinstance(arg, str): #if comes from only {path}
			var.PATH = f"{var.PATH}['{arg}']"

		var.PATHDIR = eval(f"self.data{var.PATH}")

		self.print_out()

	def case_go_to(self, loc:str):
	
		var.PATHDIR = var.PATHDIR[loc]	#go back
		var.PATH += f"{loc}/"
		self.print_out()

	def case_cd(self):
		"eg. cd"
		var.PATHDIR = self.data
		var.PATH = ""
		ret = self.print_out()
		return ret

	def caseNone(self, comm:str):
		"eg.    "
		self.not_found(comm)	#if not found

	def case_reset(self):
		"eg reset"
		print(chr(27) + "[2_j")

	def case_create_dir(self, arg:list, command="create"):
		"create"
		if len(arg) == 0 :
			return self.not_found(command, "no argument") 
		for elem in arg:
			if " " in elem: continue 
			elif len(elem) == 0: continue 
			var.PATHDIR[elem] = dict()
		self.print_out()


	def case_create_file(self, arg:list, command="add"):
		"eg add"
		if len(arg) == 0 :
			return self.not_found(command, "no argument") 

		out = []
		for elem in arg:
			if len(elem) > 0 and  not " " in elem:
				out.append(elem)
		arg = out		
		
		if len(arg)%2:
			self.not_found({arg[-1]}, " has no content" )
		
		for i in range(0, (len(arg)-1), 2 ):
			name = arg[i]
			content = arg[i+1]
			if " " in name or " " in content: continue 
			elif len(name) == 0 or len(content) == 0: continue 
			
			var.PATHDIR[name] = content
		
		self.print_out()

	def case_delete(self, arg:list):
		"eg rm"
		try:
			for elem in arg:
				del var.PATHDIR[elem]
		except:
			pass
		self.print_out()	

	def case_generate(self, arg:list):
		"eg generate [file] [passlen]"
		arg_len = len(arg)
		for i in range(0, len(arg), 2):
			if isinstance(arg[i], str):
				pass
			if i +1 < arg_len:
				if isinstance(arg[i+1], int) :
					leng = 8
				else:
					leng = arg[i+1]
			else:
				leng = 8
				pass
			passwd = self.generate(leng)
			self.case_create_file((arg[i], passwd), command="gen")
	
	


	

