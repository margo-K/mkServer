""" IRC Parts Module: 

	Classes: 
		- Message
		- Channel
		- User

"""

class Message: 
		"""IRC Compliant Message (a string) and Methods used for interpreting them

	METHODS:
		__init__ 

		<self._parse_message()> operates on a message object. returns a tuple with all the message categories. OPTIONALLY: sets the attributes of the object according to the parse
		<self._make_message()> does the opposite of parse message - it takes in a bunch of tokens and outputs a valid IRC message. The types of messages it would send include:
			1. error messages 2. confirmation-of-action-request messages (when requesting exit, nick change, etc.) 3. notifications from the server (welcome, goodbye) 4. PRIVMSGs being relayed
			OPTIONALLY : 5. responses to information requests (users, WHOIS, etc.)

		_perform_action()

	ATTRIBUTES:
		- Prefix (Optional)
		- Command
		- Command Parameters
		- Trailer (also listed as a paramater)
	(must all have methods defined above)

	IMPROVEMENTS:
		- write a real IRC parser (current is for old stand-in format)
	"""

	def __init__(self, string_message):
		"""Create an instance of message where the full message is passed in as an attribute"""
		self.value = string_message
		self.prefix = ''
		self.trailer = ''
		self.whole = (self.prefix,self.command,self.args,self.trailer)

	def parse(self):
		"""Return a tuple including the method for action being performed and the argument it accepts. Does not return if the message is malformed. Q: should it return if the message has a bad key value"""
		#print "The message being parsed is " + str(message) - does this even make sense in the current context?
		try: 
			(tag,delimiter,argument) = message.partition(' ') # Splits the action call off from the argument
		except IRCError: 
			#kill of some sort, which signals to the brain that it must send out the message to someone else

		else: 
			if prefix:
				self.prefix = ":%s"%prefix

			self.command = command
			self.args = args
			if trailer:
				self.trailer = ":%s"%trailer
			return (self.prefix,self.command,self.args,self.trailer)

		# Pure: <message,clientserver_socket> => formatted message :: <String,socketobject> => String
	def _message_maker (self): # need to get the sender nick sent as the prefix somewhere else
		"""Produce an IRC-compliant string containing the information of the message"""
		return ":{0} {1} {2} :{3}".format(self.prefix,self.command,' '.join(self.args),self.trailer) # Need to adjust for when there's no prefix or no trailer




class Channel:
	"""Contains all the information related to a channel and methods for altering those things

	ATTRIBUTES:
	- mode
	- members
	- Optionally: operators, banned list, topic
	Question: Does the name of the channel need to be inside or outside?

	METHODS: 
	- add to channel
	- delete channel
	- change mode

	"""
	def __init__ (self,founder):
		"""Creates a channel with """
		self.members = [founder]
		self.mode = []

	def add_user(self,*users):
		""" Add user(s) to the channel's list of users """
		for user in users:
			self.members.append(chan)

	def remove_user(self,*users):
		""" Remove user(s) from the channel's list of users"""
		for user in users:
			try: 
				self.members.remove(user)
			except: ValueError
			#Figure out how I want to deal with this 

	def add_mode(self,*modes):
		"""Add mode to the channel"""
		for mode in modes:
			self.mode.append(mode)

	def remove_mode(self,*modes):
		"""Remove mode from the channel"""
		for mode in modes:
			self.mode.remove(mode)ß


class User: 
	"""Contains all the identifying information about a client and the methods for altering those things

	ATTRIBUTES:
	- nickname
	- channels
	- state = [] :: binary

	METHODS:


	OPTIONAL IMPROVEMENTS:
	- make it impossible to set a nickname someone is already using (throws an error)

	 """

	######################################################################################################################
	""" 
	At some higher-up level, there must be a client directory:

	user_directory = {NICK: socket}

	"""

	def __init__(self,nickname):
		self.channels = []
		self.nick = nickname
		self.state = {username_set: 1, mode_set: 0}
 
	def is_ready(self,action):
		"""Check whether the user is ready for a given action"""

	def join_channel(self,*channels):
		"""Add channel(s) to the users list of channels"""
		for chan in channels:
			self.channels.append(chan)

	def leave_channel(self,*channels):
		""" Leave channel(s)""" 
		for chan in channels:
			try: 
				self.channels.remove(chan)
			except: ValueError
				#Need to add the error that user is not part of that channel (which is in the list of "official errors")
























