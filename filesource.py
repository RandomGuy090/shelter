import requests
import os, time
from paramiko import SSHClient, AutoAddPolicy


import variables as var

class File_source(object):

	def get_http(self, path):
		"get file from http site"
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
		client.connect(var.SSHADDR, username=var.SSHUSER, port=var.SSHPORT)
		stdin, stdout, stderr = client.exec_command(command)
		str = ""
		for line in stdout:
		    str += line
		client.close()
		return str


