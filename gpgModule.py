import gnupg, os
import variables as var

class GpgHandler():

	def __init__(self, gpghome=None):
		if gpghome == None:
			gpghome = f"{os.environ['HOME']}.gnupg/"

		try:
			self.gpg = gnupg.GPG(gnupghome=gpghome)
		except:
			print("GPG homedir error")

	def decryptSYM(self, file):
		with open(file, "rb") as f:
			content = f.read()
		data = self.gpg.decrypt(content)
		data = str(data.data, encoding="utf-8")
		return data


	def encryptSYM(self, content, file):

		data = self.gpg.encrypt(content, None, symmetric=True)
		if data.ok:
			with open(file, "wb") as f:
				f.write(data.data)
		else:
			print("error")