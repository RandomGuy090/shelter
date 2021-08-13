import configparser, os, sys
import variables as var

login = os.getlogin()

config_files = [f"/home/{login}/.config/shelter/config",
				f"/home/{login}/.shelter"]

config_template = f'''
[DEFAULT]
File_location = 
GPGHOMEDIR = /home/{login}/
SSH_port =  22
SSH_addr = 10.0.0.2
SSH_user = pi
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
				sys.exit(0)

			self.load()

	
	def load(self):
		c = configparser.ConfigParser()
		c.read_string(self.config)

		config_defaults = {
		"var.FILE": "File_location",
		"var.GPGHOMEDIR": "GPGHOMEDIR",
		"var.SSHPORT": "SSH_port",
		"var.SSHADDR": "SSH_addr",
		"var.SSHUSER": "SSH_user",
		"var.PRIV_KEY": "PRIV_KEY",
		"var.PUBLIC_KEY": "PUBLIC_KEY"
		}

	
		for elem in config_defaults:
			if eval(f" {elem} == '' "):
				s = c['DEFAULT'][config_defaults[elem]]
				res = exec(f"{elem} = '{s}'")


		if var.runSSH:
			impor = {"var.SSHUSER": var.SSHUSER,
					"var.FILE": var.FILE,
					"var.SSHPORT": var.SSHPORT,
					}
			for elem in impor:
				if impor[elem] == "":
					print(f"{config_defaults[elem]} is empty, check config file")
					sys.exit(0)


			var.FILE = f"{var.SSHUSER}@{var.SSHADDR}:{var.FILE}"
			



