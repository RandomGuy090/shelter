import random, string
import variables as var


class Generator(object):
	def generate(self, lenght):
		ret = ""
		try:
			x = int(lenght)
		except:
			x = 0

		for i in range(x):
			ind = random.randrange(len(string.ascii_letters))
			ret+= string.ascii_letters[ind]
		return ret
