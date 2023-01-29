import gnupg, os, sys
import variables as var

class Gpg_handler(object):

	def __init__(self, gpghome=None):
		if gpghome == None:
			self.gpghome = f"{os.environ['HOME']}/.gnupg"
			os.popen(f"echo 'max-cache-ttl:0:0' | GNUPGHOME='"+ '${GNUPGHOME:-' + self.gpghome + '}' +"' gpgconf --change-options gpg-agent")
			print(self.gpghome)

		try:
			self.gpg = gnupg.GPG(gnupghome=self.gpghome)
			# self.gpg = gnupg.GPG(homedir=self.gpghome, gpg="/bin/gpg")
		except Exception as e:
			print(e)
			print("GPG homedir error")
			sys.exit(-1)


	def decrypt(self, file):
		try:
			data = self.gpg.decrypt(file)
		except:
			print("xDD")

		
		if not data.ok:
			return False

		if data.key_id is not None:
			keys = self.gpg.list_keys()
			for key in keys:
				if data.key_id in key["subkeys"][0]:
					mail = key["uids"][0]
					if var.RECIP != mail:
						var.RECIP  = self.get_mail(mail)
			print(f"unencrypted with: {var.RECIP}")

		data = str(data)

		return data


	def encrypt_sym(self, content):
		data = self.gpg.encrypt(content, None, symmetric=True)
		if data.ok:
			var.CONTENT = data
			return data
		else:
			print("error")

	def encrypt_asym(self, content):
		if var.RECIP_FLAG == "self":
			fprit = self.get_fingerprit_menu(var.RECIP)
		elif var.RECIP != var.RECIP_FLAG:
			fprit = self.get_fingerprit_menu(var.RECIP_FLAG)
		elif var.RECIP == var.RECIP_FLAG:
			fprit = self.get_fingerprit_menu(var.RECIP)
		else:
			fprit = self.get_fingerprit_menu()		
			
		data = self.gpg.encrypt(content, fprit, always_trust=True)
		if data.ok:
			var.CONTENT = data
			return data
		else:
			pass

	def get_mail(self, str):
		try:
			str = str.rsplit(" ")[1][1:-1]
			return str
		except:
			pass

	def get_fingerprit_menu(self, mail=""):
		if mail == "":
			mail = self.get_mail(mail)
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
					if self.find_in_array(klist, tmp):
						mail = tmp
						break
					
		fprit = self.get_key_bymail(mail)
		return fprit

	def find_in_array(self, arr, str):
		for elem in arr:
			if elem.find(str):
				return True
				break


	def get_key_bymail(self, mail):
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
			return "_file error"

		res = self.gpg.import_keys(key)

		if res.count == 0 :
			return "import key error"
		else:
			return res.results[0]["fingerprint"]

	def delete_keys(self):
		for elem in var.DEL_KEYS:
			res = self.gpg.delete_keys(elem).status

			if res in "_must delete secret key first":
				res = self.gpg.delete_keys(elem, True, passphrase="")
				while res.status != "ok":
					passwd = input("input password of secret key: ")
					res = self.gpg.delete_keys(elem, True, passphrase=passwd)

				res = self.gpg.delete_keys(elem)


		return True





				
