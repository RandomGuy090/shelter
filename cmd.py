from shelter import Shelter
from switch import Switch
from generator import Generator
from filesource import Filesource

import variables as var

import pyperclip
import atexit, getopt, sys


class Cmd(Shelter, Switch, Generator, Filesource):

	def __init__(self, data="not used"):
		self.flags()
		self.processFileName()

		atexit.register(self.exitFuntion)
		super().__init__(var.FILE)
		self.data = var.PATHDIR
		

	def exitFuntion(self):
		"run as last, closes everything"
		var.LAST_READ = self.switch("cd")[0]
		if not var.LAST_READ == var.FIRST_READ:
			self.encrypt(var.PATHDIR)
			self.saveFile()

		self.delete_keys()

	def printOut(self)-> list:
		"returns list of 1 normal elements 2 colored elements"
		data = var.PATHDIR
		var.COMMANDS = []
		ret = list()

		for elem in data:	
			var.COMMANDS.append(elem)
			elem = self.checkType(elem, data)
			ret.append(elem)			
	
		return data, ret

	def changeColor(self, txt:str, code:"[escCde, style, txtCol, bgcol]")-> str:
		"changes color"
		header = f"{code[0]}{code[1]};{code[2]};{code[3]}m"
		tail = "\033[0;0m"
		return f"{header}{txt}{tail}"
	
	def notFound(self, command, arg="not found")-> None:
		"shows error message"
		header = f"\x1b[1;31m"
		tail = "\033[0;0m"
		print(f"{header} ERROR : '{command}' {arg}{tail}")

	def convToPath(self, path:str)->str:
		"converts [path][to] to path/to"
		path = path[2:-2]
		path = path.replace("']['", "/")
		font = [ "1", "34", "49"]

		path = self.changeColor(path, ["\x1b[",font[0] ,font[1],font[2]])
		return path

	def promptColor(self, str:str)-> str:
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
		info = self.changeColor(info, ["\x1b[",font[0] ,font[1],font[2]])


	def processFileName(self):
		if var.FILE.startswith("http"):
			"if http address is given in the -f flag"
			var.CONTENT = self.getHttp()

		elif "@" in var.FILE:
			"if ssh address is given in the -f flag"
			user, adr = var.FILE.split("@") 
			adr, var.SSHPATH = adr.split(":")
			var.FILE = f"{user}@{adr} -p {var.SSHPORT}"
			var.CONTENT = self.getSSH()

		else:
			var.CONTENT = self.readFile()

	
	def flags(self):
		try:
			argv = sys.argv[1:]
			options, reminder = getopt.getopt(argv,"f:r:h:s:p:P:",["file=","recip=", "help=", \
								"public=", "secret=","port"])

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
				elif opt in ("-P", "--port"):
					var.SSHPORT = arg

				elif opt in ("-h", "--help"):
					self.printHelp()
					sys.exit(0)

		except getopt.GetoptError as e:
			self.printHelp()
			sys.exit(0)
	
	def printHelp(self):
		"help printout"
		print(""" ./shelter.py <options>
	   -f --file 		file location
	   -r --recipient	recipient       
	   -s --secret		import secret key
	   -p --public		import public key
	   -P --port 		ssh server port

	   e.g.
	   with ssh server
	   ./run.py -f <user>@<ip>:<path/to/file> -P <port> 
	   with http server
	   ./run.py -f <http://path/to/file> 

	   import keys
	   ./run.py -f <path> -p <path/to/pubkey> -s <path/to/prv/key>
	
		change recipient (after commited changes)
	   
	   ./run.py -f <path> -r <email>

		""")





		
		
