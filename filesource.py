import requests
import os, time, sys
from paramiko import SSHClient, AutoAddPolicy


import variables as var

class File_source(object):

	def get_http(self, path):
		"get file from http site"
		var.FILE = f"http://{var.FILE}"
		print(var.FILE)
		tmp = requests.get(var.FILE).text
		return tmp
	
	def get_ssh(self):
		"get file from ssh server"
		return self.ssh_pipe(f"cat {var.SSHPATH}")


	def save_ssh(self):
		"save file from ssh server"
		com = f"echo '{var.CONTENT}' > {var.SSHPATH}"
		self.ssh_pipe(com)
	
	def ssh_pipe(selfm, command):
		"function creating and closing ssh pipe"

		client = SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(AutoAddPolicy())
		print(var.SSHADDR)
		print(var.SSHUSER)
		print(var.SSHPORT)
		try:
			client.connect(var.SSHADDR, username=var.SSHUSER, port=var.SSHPORT)
		except:
			# raise Exception("xD")
			sys.exit(-1)
			# print("could not connect")

		stdin, stdout, stderr = client.exec_command(command)
		str = ""
		for line in stdout:
		    str += line
		client.close()
		return str


