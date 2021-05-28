import gnupg, os
import variables as var

class GpgHandler(object):

	def __init__(self, gpghome=None):
		if gpghome == None:
			gpghome = f"{os.environ['HOME']}.gnupg/"

		try:
			self.gpg = gnupg.GPG(gnupghome=gpghome)
		except:
			print("GPG homedir error")

	def decrypt(self, file):
		with open(file, "rb") as f:
			content = f.read()

		data = self.gpg.decrypt(content)
		if data.key_id is not None:
			keys = self.gpg.list_keys()
			for key in keys:
				if data.key_id in key["subkeys"][0]:
					mail = key["uids"][0]
					if var.RECIP != mail:
						var.RECIP  = self.getMail(mail )

		data = str(data.data, encoding="utf-8")
		return data


	def encryptSYM(self, content, file):
		data = self.gpg.encrypt(content, None, symmetric=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			print("error")

	def encrypt_ASYM(self, content, file):
		print(f"{var.RECIP}  {var.RECIP_FLAG}")

		if var.RECIP_FLAG == "self":
			fprit = self.getFingerpritMenu(var.RECIP)
		elif var.RECIP != var.RECIP_FLAG:
			fprit = self.getFingerpritMenu(var.RECIP_FLAG)
		else:
			fprit = self.getFingerpritMenu()		
			
		data = self.gpg.encrypt(content, fprit, always_trust=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			pass

	def getMail(self, str):

		try:
			str = str.rsplit(" ")[1][1:-1]
			return str
		except:
			pass

	def getFingerpritMenu(self, mail=""):
		if mail == "":
			mail = self.getMail(mail)
			keys = self.gpg.list_keys()
			klist = list()
			for key in keys:
				for elem in key["uids"]:
					print(f" ----->  {elem}")
					klist.append(elem)
					elem = elem[elem.index("<")+1:-1]
					var.COMMANDS.append(elem)
			if mail not in klist:
				mail = input("input mail:  ")

		fprit = self.getKeyBymail(mail)
		return fprit


	def getKeyBymail(self, mail):
		keys = self.gpg.list_keys()

		mail = mail.split(" ")[0]

		for key in keys:
			if mail in key["uids"][0]:
				return key["fingerprint"]







				
