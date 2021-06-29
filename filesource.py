import requests
import variables as var
import os

class Filesource(object):
	def getHttp(self, path):
		"get file from http site"
		tmp = requests.get(var.FILE).text
		return tmp
	
	def getSSH(self):
		"get file from ssh server"
		val = os.popen(f"ssh {var.FILE} 'cat {var.SSHPATH}'").read()
		return val

	def saveSSH(self):
		"save file from ssh server"
		com = f"echo '{var.CONTENT}' > {var.SSHPATH}"
		val = os.popen(f'ssh {var.FILE} "{com}"').read()
		# print(f"ssh {var.FILE} {com}")
	
	def test(self):
		print("test")

