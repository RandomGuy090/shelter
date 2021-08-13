import copy
import variables as var


class import_csv():
	def import_from_csv(self):
		
		self.txt = ""
		self.read()
		self.get_headers()
		self.change_to_dict()
		self.form_to_shelter()
		# for elem in self.txt :
		# 	print(f"{self.txt[elem]['login']}  {self.txt[elem]['password']}")
		return self.txt

	def read(self):
		with open(var.IMPORT_FILE, "rt" ) as f:
			self.txt = f.read()
			self.txt = self.txt.replace('"', "")

		return self.txt

	def get_headers(self):
		self.txt = self.txt.rsplit("\n")
		self.headers = self.txt[0].rsplit(",")
		self.txt = self.txt[1:]


	def change_to_dict(self):
		ret = list()
		for elem in self.txt:
			row = elem.rsplit(",")
			# print(dict(zip(self.headers, elem)))
			# print(elem)
			ret.append(dict(zip(self.headers, row)))
		self.txt = ret
		return ret

	def form_to_shelter(self):
		ret = dict()
		for elem in self.txt:
			print(elem)
			try:
				ret[elem["name"]] = {
				"login": elem["username"],
				"password": elem["password"]
				}
			except:
				ret[elem["url"]] = {
				"login": elem["username"],
				"password": elem["password"]
				}
		self.txt = ret
		return ret





import_csv()