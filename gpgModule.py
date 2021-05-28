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
					print(f"unencrypted with: {var.RECIP}")

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
		mail = var.RECIP.rsplit(" ")[1][1:-1]
		data = self.gpg.encrypt(content, mail, always_trust=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			print("error")




				
