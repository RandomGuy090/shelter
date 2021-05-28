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
					print(f"unencrypted with: {mail}")
					if var.RECIP != mail:
						mail = var.RECIP 

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
		mail = self.getMail(var.RECIP)

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

		print(mail)
		data = self.gpg.encrypt(content, [mail], always_trust=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			print(data.status)
			print("error")

	def getMail(self, str):
		try:
			str = str.rsplit(" ")[1][1:-1]
		except:
			pass
		return str

	def getKeyBymail(self, mail):
		keys = self.gpg.list_keys()
		for key in keys:
			for mail in key["uids"]:
				print(key[keyid])
				break







				
