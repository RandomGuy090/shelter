import random, string
import variables as var


class Generator(object):
	def generate(self, lenght):
		ret = ""
		for i in range(int(lenght)):
			ind = random.randrange(len(string.ascii_letters))
			ret+= string.ascii_letters[ind]
		return ret
