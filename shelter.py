from gpgModule import Gpg_handler
import gnupg, json, copy, sys, os
import variables as var

from import_csv import import_csv as csv




class Shelter(csv):
	buffer = None
	
	def __init__(self, path:str):
		if var.PRIV_KEY:
			if self.import_key(var.PRIV_KEY) != "ok":
				self.failure_exit("importing key error")

		if var.PUBLIC_KEY:
			if self.import_key(var.PUBLIC_KEY) != "ok":
				self.failure_exit("importing key error")
		
		if not var.PATHDIR: 
			self.decrypt()
				
	def failure_exit(self, command="")->None:
		print(f"shelter error  {command}")
		sys.exit(1)

	def return_false(self):
		return False

	def parse_json(self, txt:str)->"str/dict":
		"parse to/from json"
		if txt == "":
			self.failure_exit("decoding error")
		if isinstance(txt, dict):
			return json.dumps(txt)
		else:
			return json.loads(txt)

	def check_type(self, txt:str, elem:str)->str:
		"checks type of element and colors it"
		font1 = [ "1", "34", "49"]
		font2 = [ "1", "33", "49"]
		if isinstance(elem[txt], dict):
			txt = self.change_color(txt, ["\x1b[",font1[0] ,font1[1],font1[2]])

		elif isinstance(elem[txt], str):
			txt = self.change_color(txt, ["\x1b[", font2[0], font2[1], font2[2]])		
		return txt	

	def read_file(self):
		"read file"
		with open(var.FILE, "rt") as f:
			content = f.read()
			return content

	def decrypt(self)->str:		#prepare and call gpg handler to decrypt
		"decrypts file"			

		tmp = Gpg_handler().decrypt(var.CONTENT)
		if not tmp:
			print("File broken")
			self.failure_exit("file not decrypted")
		tmp = self.parse_json(tmp)

		var.FIRST_READ = copy.deepcopy(tmp)		#compare later if user made any changes
		var.PATHDIR = tmp
	
	def encrypt(self, content)->str:		#prepare and call gpg handler to decrypt
		"encrypts file"
		
		tmp = self.parse_json(content)
		if var.RECIP == "" and var.RECIP_FLAG == "":
			Gpg_handler().encrypt_sym(tmp)
		else:
			Gpg_handler().encrypt_asym(tmp)


	def save_file(self):
		"saving encrypted file"		
		if var.FILE.startswith("http"):
			print("cannot save in http mode")
			self.failure_exit("cannot save in http source mode")
			#extend here with prompt asking for new file location
			return 

		if "@" in var.FILE:
			self.save_ssh()
			return 

		with open(var.FILE, "w") as f:
			var.CONTENT = str(var.CONTENT)
			f.write(var.CONTENT)


	def import_key(self, file):
		"import keys from flags"
		res = Gpg_handler().import_key(file)
		if "error" not in res:
			var.DEL_KEYS.append(res)
			return "ok"
		else: 
			return "error"
	
	def delete_keys(self):
		return Gpg_handler().delete_keys()

	def csv(self):
		tmp = self.import_from_csv()
		# tmp = self.parse_json(tmp)
		var.FIRST_READ = copy.copy(tmp)		#compare later if user made any changes
		var.PATHDIR = dict(tmp)
		# print(var.PATHDIR)


