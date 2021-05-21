from gpgModule import GpgHandler
import gnupg, json, copy, sys, os
import variables as var



class Shelter(object):
	buffer = None
	
	def __init__(self, path):
		if not os.path.isfile(path):
			self.failureExit("bad input file")

		var.PATHDIR = GpgHandler().decrypt(path)
		var.PATHDIR = self.parseJSON(var.PATHDIR)
		var.FIRST_READ = var.PATHDIR		#compare later if user made any changes

		
	def failureExit(self, command):
		print("GPG init file error")
		sys.exit(1)


	def returnFalse(self):
		return False

	def parseJSON(self, txt):
		return json.loads(txt)

	def decrypt(self, file):
		with open(file, "rt") as f:
			## decrypt with gpg here
			tmp = self.parseJSON(f.read())
			self.buffer = tmp
			return tmp

	def checkType(self, txt, elem)->"dict":
		font1 = [ "1", "34", "49"]
		font2 = [ "1", "33", "49"]
		if isinstance(elem[txt], dict):
			txt = self.changeColor(txt, ["\x1b[",font1[0] ,font1[1],font1[2]])

		elif isinstance(elem[txt], str):
			txt = self.changeColor(txt, ["\x1b[", font2[0], font2[1], font2[2]])
		
		return txt	

