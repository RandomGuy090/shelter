import requests
import os, time
from paramiko import SSHClient, AutoAddPolicy

import variables as var

class Filesource(object):

	def getHttp(self, path):
		"get file from http site"
		tmp = requests.get(var.FILE).text
		return tmp
	
	def getSSH(self):
		"get file from ssh server"
		# val = os.popen(f"ssh {var.FILE} 'cat {var.SSHPATH}'").read()
		# return val
		return self.sshPipe(f"cat {var.SSHPATH}")


	def saveSSH(self):
		"save file from ssh server"
		com = f"echo '{var.CONTENT}' > {var.SSHPATH}"

		self.sshPipe(com)
	
	def sshPipe(selfm, command):
		"function creating and closing ssh pipe"
		client = SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(AutoAddPolicy())

		client.connect(var.SSHADDR, username=var.SSHUSER, port=var.SSHPORT)
		stdin, stdout, stderr = client.exec_command(command)

		str = ""
		for line in stdout:
		    str += line
		client.close()
		return str

	def test(self):
		print("test")

