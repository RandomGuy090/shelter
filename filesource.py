import requests
import variables as var

class Filesource(object):
	def getHttp(self, path):
		tmp = requests.get(path).text
		return tmp