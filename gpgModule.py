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

	def decrypt(self, file):
		with open(file, "rb") as f:
			content = f.read()
		data = self.gpg.decrypt(content)
		data = str(data.data, encoding="utf-8")
		return data