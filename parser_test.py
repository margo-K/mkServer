import unittest
from ircparts import Message

class Parser_Tests(unittest.TestCase):
	""" Test the correctness of the parser function in the Message class of the ircparts module""

	"""

	def setUp(self):
		self.m = Message()
		pass

	def test_basic_parse(self):
		message = ":prefix COMMAND arg1 arg2 arg3 :This should be a properly formatted IRCMessage : :"
		target = ('prefix','COMMAND',['arg1','arg2','arg3'],'This should be a properly formatted IRCMessage : :')

		print self.m._parse(message)

		self.assertEquals(self.m._parse(message),target)

	def test_parse2(self):
		message = "COMMAND arg1 arg2 :Some stuff"
		target = ('','COMMAND',['arg1','arg2'],'Some stuff')
		print self.m._parse(message)

		self.assertEquals(self.m._parse(message),target)


	def test_parse3(self):
		message = ":prefix and some stuff COMMAND arg1"
		target = ('prefix and some stuff','COMMAND','arg1','')
		print self.m._parse(message)

		self.assertEquals(self.m._parse(message),target)



if __name__ == '__main__':
	unittest.main()
