from gpgModule import GpgHandler
import gnupg, json, copy, sys, os
import variables as var



class Shelter(object):
	buffer = None
	
	def __init__(self, path:str):
		if not os.path.isfile(path):
			self.failureExit("bad input file")

		var.PATHDIR = self.decrypt(path)
		
	def failureExit(self, command:str)->None:
		print("GPG init file error")
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

	def decrypt(self, file:"path to file")->str:		#prepare and call gpg handler to decrypt
		"decrypts file"
		tmp = GpgHandler().decrypt(file)

		tmp = self.parseJSON(tmp)

		var.FIRST_READ = copy.copy(tmp)		#compare later if user made any changes
		return tmp
	
	def encrypt(self, content, file:"path to file")->str:		#prepare and call gpg handler to decrypt
		"encrypts file"

		tmp = self.parseJSON(content)
		if var.LAST_READ == var.FIRST_READ:
			print("exit, no save")
			return
		print(var.RECIP)
		print(var.RECIP_FLAG)
		if var.RECIP == "" and var.RECIP_FLAG == "":
			tmp = GpgHandler().encryptSYM(tmp, file)
		else:
			tmp = GpgHandler().encrypt_ASYM(tmp, file)

		return tmp

	def import_key(self, file):
		res = GpgHandler().import_key(file)
		if "error" not in res:
			var.DEL_KEYS.append(res)
			return "ok"
		else: 
			return "error"
	def delete_keys(self):
		return GpgHandler().delete_keys()

