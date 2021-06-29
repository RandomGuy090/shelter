import gnupg, os
import variables as var

class GpgHandler(object):

	def __init__(self, gpghome=None):
		if gpghome == None:
			self.gpghome = f"{os.environ['HOME']}.gnupg/"

		try:
			self.gpg = gnupg.GPG(gnupghome=gpghome)
		except:
			print("GPG homedir error")


	def decrypt(self, file):

		data = self.gpg.decrypt(file)
		
		if not data.ok:
			return False

		if data.key_id is not None:
			keys = self.gpg.list_keys()
			for key in keys:
				if data.key_id in key["subkeys"][0]:
					mail = key["uids"][0]
					if var.RECIP != mail:
						var.RECIP  = self.getMail(mail)
			print(f"unencrypted with: {var.RECIP}")


		data = str(data)

		return data


	def encryptSYM(self, content, file):
		data = self.gpg.encrypt(content, None, symmetric=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			print("error")

	def encrypt_ASYM(self, content, file):
		if var.RECIP_FLAG == "self":
			fprit = self.getFingerpritMenu(var.RECIP)
		elif var.RECIP != var.RECIP_FLAG:
			fprit = self.getFingerpritMenu(var.RECIP_FLAG)
		elif var.RECIP == var.RECIP_FLAG:
			fprit = self.getFingerpritMenu(var.RECIP)
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
				while True:
					tmp = input("input mail:  ")
					if tmp == "":
						mail = var.RECIP
						break
					if self.findInArray(klist, tmp):
						mail = tmp
						break
					
		fprit = self.getKeyBymail(mail)
		return fprit

	def findInArray(self, arr, str):
		for elem in arr:
			if elem.find(str):
				return True
				break


	def getKeyBymail(self, mail):
		keys = self.gpg.list_keys()

		mail = mail.split(" ")[0]

		for key in keys:
			if mail in key["uids"][0]:
				return key["fingerprint"]

	def import_key(self, file):
		"gpg handler to import keys"
		try:
			with open(file, "rt") as f:
				key = f.read()
		except:
			return "File error"

		res = self.gpg.import_keys(key, passphrase="ASDwer4852")

		if res.count == 0 :
			return "import key error"
		else:
			return res.results[0]["fingerprint"]

	def delete_keys(self):
		for elem in var.DEL_KEYS:
			res = self.gpg.delete_keys(elem).status

			if res in "Must delete secret key first":
				res = self.gpg.delete_keys(elem, True, passphrase="")
				while res.status != "ok":
					passwd = input("input password of secret key: ")
					res = self.gpg.delete_keys(elem, True, passphrase=passwd)

				res = self.gpg.delete_keys(elem)

			# elif res == "No such key":
			# 	print(" NO SUCH KEY")

		return True





				
