from shelter import Shelter
from switch import Switch
from generator import Generator
from filesource import File_source
from config import Config

import variables as var

import pyperclip
import atexit, getopt, sys


class Cmd(Shelter, Switch, Generator, File_source):

	def __init__(self, data="not used"):

		self.flags()
		Config()
		if not var.PATHDIR:
			self.process_file_name()


		atexit.register(self.exit_funtion)
		super().__init__(var.FILE)

		self.data = var.PATHDIR
		

	def exit_funtion(self):
		"run as last, closes everything"
		try:
			var.LAST_READ = self.switch("cd")[0]
		except:
			print(f"_file -- {var.FILE} -- has no content, \nclosing....")
			return
		if not var.LAST_READ == var.FIRST_READ or var.IMPORT_FILE:
			if var.FILE == "":
				var.FILE = input(self.prompt_color("insert file name >: "))

			self.encrypt(var.PATHDIR)
			self.save_file()

		self.delete_keys()

	def print_out(self)-> list:
		"returns list of 1 normal elements 2 colored elements"
		data = var.PATHDIR
		var.COMMANDS = []
		ret = list()

		for elem in data:	
			var.COMMANDS.append(elem)
			elem = self.check_type(elem, data)
			ret.append(elem)			
	
		return data, ret

	def change_color(self, txt:str, code:"[esc_cde, style, txt_col, bgcol]")-> str:
		"changes color"
		header = f"{code[0]}{code[1]};{code[2]};{code[3]}m"
		tail = "\033[0;0m"
		return f"{header}{txt}{tail}"
	
	def not_found(self, command, arg="not found")-> None:
		"shows error message"
		header = f"\x1b[1;31m"
		tail = "\033[0;0m"
		print(f"{header} Error : '{command}' {arg}{tail}")

	def conv_to_path(self, path:str)->str:
		"converts [path][to] to path/to"
		path = path[2:-2]
		path = path.replace("']['", "/")
		font = [ "1", "34", "49"]

		path = self.change_color(path, ["\x1b[",font[0] ,font[1],font[2]])
		return path

	def prompt_color(self, str:str)-> str:
		"returns coloured prompt"
		header = f"\x1b[1;32m"
		tail = "\033[0;0m"
		return f"{header}{str}{tail}"

	def clipboard(self, passwd:str)-> None:
		"copy to clipboard"
		pyperclip.copy(passwd)
		self.copied()

	def copied(self)-> None:
		"show copied passwd info"
		font = [ "1", "31", "49"]
		info = "--> password copied <--"
		info = self.change_color(info, ["\x1b[",font[0] ,font[1],font[2]])
		print(info)


	def process_file_name(self):
		print(var.FILE)
		if var.FILE.startswith("http"):
			"if http address is given in the -f flag"
			var.CONTENT = self.get_http()

		elif "@" in var.FILE:
			"if ssh address is given in the -f flag"
			var.SSHUSER, adr = var.FILE.split("@") 
			var.SSHADDR, var.SSHPATH = adr.split(":")
			var.CONTENT = self.get_ssh()

		else:
			var.CONTENT = self.read_file()

	
	def flags(self):
		try:
			argv = sys.argv[1:]
			options, reminder = getopt.getopt(argv,"f:r:h:s:p:_p:c:i:",["file=","recip=", "help=", \
								"public=", "secret=","port", "config", "import"])

			for opt, arg in options:
				if opt in ('-f', '--file'):
					var.FILE = arg
					# var.FILE = arg
				elif opt in ('-r', '--recip'):
					var.RECIP_FLAG = arg
				elif opt in ("-s", "--secret"):
					var.PRIV_KEY = arg
				elif opt in ("-p", "--public"):
					var.PUBLIC_KEY = arg
				elif opt in ("-_p", "--port"):
					var.SSHPORT = arg
				elif opt in ("-c", "--config"):
					print(f"config file {arg}")
					var.CONFIG_FILES.append(arg)
				elif opt in ("-i", "--import"):
					var.IMPORT_FILE = arg
					tmp = self.csv()
					


				elif opt in ("-h", "--help"):
					self.print_help()
					sys.exit(0)

			if "ssh" in argv:
				print("ssh in args, connecting default ssh server")
				var.runSSH = True


		except getopt.GetoptError as e:
			self.print_help()
			sys.exit(0)
	
	def print_help(self):
		"help printout"
		print(""" ./shelter.py <options>
	   -f --file 		file location
	   -r --recipient	recipient       
	   -s --secret		import secret key
	   -p --public		import public key
	   -_p --port 		ssh server port

	   e.g.
	   with ssh server
	   ./run.py -f <user>@<ip>:<path/to/file> -_p <port> 
	   or 
	   ./run.py ssh
	   if important variables are defined in config file 

	   with http server
	   ./run.py -f <http://path/to/file> 

	   import keys
	   ./run.py -f <path> -p <path/to/pubkey> -s <path/to/prv/key>
	
		change recipient (after commited changes)
	   
	   ./run.py -f <path> -r <email>

		""")





		
		
