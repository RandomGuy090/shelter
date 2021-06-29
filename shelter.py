from gpgModule import GpgHandler
import gnupg, json, copy, sys, os
import variables as var



class Shelter(object):
	buffer = None
	
	def __init__(self, path:str):
		# if not os.path.isfile(path):
		# 	self.failureExit("bad input file")

		if var.PRIV_KEY:
			if self.import_key(var.PRIV_KEY) != "ok":
				self.failureExit("importing key error")

		if var.PUBLIC_KEY:
			if self.import_key(var.PUBLIC_KEY) != "ok":
				self.failureExit("importing key error")
		
		var.PATHDIR = self.decrypt()

		
	def failureExit(self, command="")->None:
		print(f"GPG init file error  {command}")
		sys.exit(1)

	def returnFalse(self):
		return False

	def parseJSON(self, txt:str)->"str/dict":
		"parse to/from json"
		if txt == "":
			self.failureExit("decoding error")
		if isinstance(txt, dict):
			return json.dumps(txt)
		else:
			return json.loads(txt)

	def checkType(self, txt:str, elem:str)->str:
		"checks type of element and colors it"
		font1 = [ "1", "34", "49"]
		font2 = [ "1", "33", "49"]
		if isinstance(elem[txt], dict):
			txt = self.changeColor(txt, ["\x1b[",font1[0] ,font1[1],font1[2]])

		elif isinstance(elem[txt], str):
			txt = self.changeColor(txt, ["\x1b[", font2[0], font2[1], font2[2]])		
		return txt	

	def readFile(self):
		"read file"
		with open(var.FILE, "rt") as f:
			content = f.read()
			return content

	def decrypt(self)->str:		#prepare and call gpg handler to decrypt
		"decrypts file"			

		tmp = GpgHandler().decrypt(var.CONTENT)
		if not tmp:
			self.failureExit("file not decrypted")
		tmp = self.parseJSON(tmp)

		var.FIRST_READ = copy.copy(tmp)		#compare later if user made any changes
		return tmp
	
	def encrypt(self, content)->str:		#prepare and call gpg handler to decrypt
		"encrypts file"
		
		tmp = self.parseJSON(content)
		
		
		if var.RECIP == "" and var.RECIP_FLAG == "":
			GpgHandler().encryptSYM(tmp)
		else:
			GpgHandler().encrypt_ASYM(tmp)


	def saveFile(self):
		"saving encrypted file"		
		if var.FILE.startswith("http"):
			print("cannot save in http mode")
			self.failureExit("cannot save in http source mode")
			#extend here with prompt asking for new file location
			return 

		if "@" in var.FILE:
			self.saveSSH()
			return 

		with open(var.FILE, "w") as f:
			var.CONTENT = str(var.CONTENT)
			f.write(var.CONTENT)


	def import_key(self, file):
		"import keys from flags"
		res = GpgHandler().import_key(file)
		if "error" not in res:
			var.DEL_KEYS.append(res)
			return "ok"
		else: 
			return "error"
	
	def delete_keys(self):
		return GpgHandler().delete_keys()

