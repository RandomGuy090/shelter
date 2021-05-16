import gnupg, json, copy
class Shelter(object):
	buffer = None
	
	def parseJSON(self, txt):
		return json.loads(txt)

	def decrypt(self, file):
		with open(file, "rt") as f:
			## decrypt with gpg here
			tmp = self.parseJSON(f.read())
			self.buffer = tmp
			return tmp

	def checkType(self, txt, elem)->"dict":
		font1 = [ "1", "37", "42"]
		font2 = [ "1", "30", "41"]
		if isinstance(elem[txt], dict):
			txt = self.changeColor(txt, ["\x1b[",font1[0] ,font1[1],font1[2]])

		elif isinstance(elem[txt], str):
			txt = self.changeColor(txt, ["\x1b[", font2[0], font2[1], font2[2]])
		
		return txt	


	def changeColor(self, txt, code:"[escCde, style, txtCol, bgcol]")-> "colored string":
		header = f"{code[0]}{code[1]};{code[2]};{code[3]}m"
		tail = "\033[0;0m"
		return f"{header}{txt}{tail}"

	def list(self, data):
		for elem in data:	
			elem = self.checkType(elem, data)
			print(elem)
