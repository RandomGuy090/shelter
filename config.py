import configparser, os
import variables as var

login = os.getlogin()

config_files = [f"/home/{login}/.config/shelter/config",
				f"/home/{login}/.shelter"]

config_template = f'''
[DEFAULT]
File_location = 
GPGHOMEDIR = /home/{login}/
SSH_port = 
SSH_addr = 
PRIV_KEY = 
PUBLIC_KEY = 

'''

class Config(object):
	config = ""
	def __init__(self, file=None):
		if file == None:
			for elem in config_files:
				try:
					f = open(elem, 'r')
					self.config = f.read()
				except:
					pass
			if self.config == "":
				print("no config file, creating new")
				print("create: ")
				print(config_files[0])
				try:

					os.makedirs(os.path.dirname(config_files[0]), exist_ok=True)
					f = open(config_files[0], 'w+')
					f.write(config_template)
				except:
					print("error creating")

			self.load()

	
	def load(self):
		c = configparser.ConfigParser()
		c.read_string(self.config)
		
		if var.FILE == "":
			var.FILE = c["DEFAULT"]["File_location"]

		if var.GPGHOMEDIR == "":
			var.GPGHOMEDIR = c["DEFAULT"]["GPGHOMEDIR"]

		if var.SSHPORT == "":
			var.SSHPORT = c["DEFAULT"]["SSH_port"]
			
		if var.SSHADDR == "":
			var.SSHADDR = c["DEFAULT"]["SSH_addr"]

		if var.PRIV_KEY == "":
			var.PRIV_KEY = c["DEFAULT"]["PRIV_KEY"]

		if var.PUBLIC_KEY == "":
			var.PUBLIC_KEY = c["DEFAULT"]["PUBLIC_KEY"]
		



