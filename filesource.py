import requests
import variables as var
import os

class Filesource(object):
	def getHttp(self, path):
		"get file from http site"
		tmp = requests.get(var.FILE).text
		return tmp
	
	def getSSH(self, path):
		"get file from ssh server"
		print("ssh")
		val = os.popen(f"ssh {var.FILE} 'cat {path}'").read()
		return val