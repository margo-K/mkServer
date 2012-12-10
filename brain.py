class Brain():
	"""The brain primarily functions as the "MAILMAN", with a few added attributes that help with this task:

			MAILMAN: The mailmain looks at the messages that come in (of the form [P,C,Args,Trailer]) and directs them to where they're supposed to go.
			
			Each individual object that the brain routes stuff to (Users, Messages, Channels) only need to see the things related to their part of the task - and the brain or the ("mailman") just
			makes sure that the proper object gets the task - and that any side effects that interact with other "ideas" in the brain get routed there, in the form of steps linked together that interact act with all the parts of the brain that are affected by a given action (sends an error message, )

			ATTRIBUTES:
				- self.username_dictionary: a dictionary of usernames with the connection object for each one (tcp sockets, etc.) as the keys
				- self.action_dictionary: 

			METHODS:
				- Helper Functions:
				- Messaging Operations:
				- User Operations:
				- Channel Operations:

				- The Meat: self.process()
					The only function called externally by mkServer


	"""

	def __init__(self):
		"""Create the initial environment for a functioning brain"""
		self.username_directory = {}  #keys=usernames; entries: the connection object for each one (where the messages will be sent/received from)
		self.action_dictionary = {"NICK": self._store_username, "MODE": self._mode_change, "USER":self._set_user, "PRIVMSG":self._ping, "JOIN":self._join_channel, "PART":self._part_channel, "QUIT": self._client_terminate}# may be unnecessary later 

	######################################################################################################################
					#Helper Functions#
					#mostly unnecessary in the finished program#
	######################################################################################################################
	def _start_counter(self):
		"""Initiates the counter used below"""
		self.counter = 0
		
	def _counter(self):
		"""Returns the next number in a sequence"""
		self.counter +=1
		return self.counter

	def username_generator(self):
		"""Generate a sequential list of usernames"""
		return 'User %s'%self._counter()

	def _or_set(self,field,fn):
		"""Return field or the value returned by the fn if field is none"""
		if field is None:
			return fn()
		else: 
			return field

	def return_messages(self,msg,destination):
		"""Return a list of tuples of the form (msg,destination)"""
		messages = []
		for recipient in destination:
			messages.append((msg,recipient))
		return messages
 
	######################################################################################################################
					#Messaging Operations#
	######################################################################################################################
	def _ping(self,clientserver_socket,message):
		"""Called when a message is sent from the clientserver_socket"""
		self.message_queue.put((message,clientserver_socket))


	######################################################################################################################
					#User Operations#
	######################################################################################################################
	def _store_username(self,clientserver_socket,username=None):
		"""Store a client's username in the username dictionary"""
		# if username:
		# 	screenname = screenname
		# else:
		# 	screenname = self.username_generator()
		screenname = self._or_set(username,self.username_generator)

		self.username_directory[screenname] = clientserver_socket
		print screenname + " has been stored as a username." 

	def _set_user(self,user,*args):
		"""Set the user """
		pass

	def _mode_change(self,user,mode): 
		user.setmode(mode)

	def _client_terminate(self,clientserver_socket,exit_message = "Client Exiting"):
		"""Close the client's socket"""
		addr = clientserver_socket.getpeername()
		usn = self.username_directory[clientserver_socket]
		self.current_sockets.remove(clientserver_socket)

		clientserver_socket.close()
		print (exit_message + "Client %s Removed at %s") % (usn,addr)

	######################################################################################################################
					#Channel Operations#
	######################################################################################################################
	def _join_channel(self,user,*channel):
		for c in channel:
			c.add(user)

	def _part_channel(self,user,*channel):
		for c in channel:
			c.delete(user)

	######################################################################################################################
					#Brain Meat#
	######################################################################################################################
	def process(self,message,source):
		""" 1. Sends the message to get parsed by the MESSAGE (no matter what) & returns if it's a valid IRC MESSAGE. Throws an error if not
			2. Returns the message if it's a valid IRC message tries to perform action (by looking up the action in the username dictionary)
			3. Tries to perform the action & returns an error if it can't (as a message to be sent out)ß 

		Take a message and perform the action requested, if possible. Return a list of messages that must be sent out """
		"""pseudocode for what should happen:
		1. the brain checks whether the source is already a user, if not, it makes a user
		2. then it checks if the source is 'ready' for what it's asking to do. the disadvantage of having the user handle the message is that then the other actions that are really outside of itself must be performed by it - instead of the brain calling other components to handle it - 
		it shouldn't need to know what to do - just how it's feeling and what it's ready for
		3. then it tries to do what it's asking to do and generates exceptions and error messages if it can't (and stores it in message to be sent out)

		"""
		# current_message = Message(message)
		# current_message.parse()
		
		if source not in self.username_directory: 
			self._store_username(source)
		recipients = self.username_directory.values()
		if source in recipients:
			recipients.remove(source)

		return self.return_messages(message,recipients) 

		#The most basic way handle can work is it does nothing but relays so:
		# (msg, source) => (msg,other1),(msg,other2), where others = anyone who has sent a message already
