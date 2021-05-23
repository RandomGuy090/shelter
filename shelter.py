from gpgModule import GpgHandler
import gnupg, json, copy, sys, os
import variables as var



class Shelter(object):
	buffer = None
	
	def __init__(self, path):
		if not os.path.isfile(path):
			self.failureExit("bad input file")

		var.PATHDIR = self.decrypt(path)
		

	def failureExit(self, command):
		print("GPG init file error")
		sys.exit(1)


	def returnFalse(self):
		return False

	def parseJSON(self, txt):
		if isinstance(txt, dict):
			return json.dumps(txt)
		else:
			return json.loads(txt)


	def checkType(self, txt, elem)->"dict":
		font1 = [ "1", "34", "49"]
		font2 = [ "1", "33", "49"]
		if isinstance(elem[txt], dict):
			txt = self.changeColor(txt, ["\x1b[",font1[0] ,font1[1],font1[2]])

		elif isinstance(elem[txt], str):
			txt = self.changeColor(txt, ["\x1b[", font2[0], font2[1], font2[2]])		
		return txt	

	def decrypt(self, file):		#prepare and call gpg handler to decrypt
		tmp = GpgHandler().decryptSYM(file)
		tmp = self.parseJSON(tmp)
		
		var.FIRST_READ = copy.copy(tmp)		#compare later if user made any changes
		return tmp

	
	def encrypt(self, content, file):		#prepare and call gpg handler to decrypt
		tmp = self.parseJSON(content)
		if var.LAST_READ == var.FIRST_READ:
			print("exit, no save")
			return

		tmp = GpgHandler().encryptSYM(tmp, file)
		return tmp
