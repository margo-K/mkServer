import Channel, Message_Manager,Message,User from ircparts

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
					*The only function called externally by mkServer; must return a list of messages of the form (message, destination),
					where destination is the actual socket (or whatever 'tin can' the client has)

	"""

	def __init__(self):
		"""Create the initial environment for a functioning brain"""
		self.username_directory = {}  #keys=usernames; entries: the connection object for each one (where the messages will be sent/received from)
		self.action_dictionary = {"NICK": self._store_username, "MODE": self._mode_change, "USER":self._set_user, "PRIVMSG":self._ping, "JOIN":self._join_channel, "PART":self._part_channel, "QUIT": self._client_terminate}# may be unnecessary later 
		self.message_man = Message_Manager()

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

	def careful_call(fn):
		"""Call the function being careful that it's okay to call it (based on the user)"""
 
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
	def process(self,unformatted_message,source):
		""" Process individual message strings, perform necessary actions and return a list of error and/or confirmation messages 
		Called by the Server
		"""
		outgoing_messages = []

		try:
		(prefix, command, args, trailer) = self.message_man.parse(unformatted_message) # prefix can be ignored for incoming messages
		except TypeError:
			print "The message was not a valid IRCMessage" 

		action = self.action_dictionary[command]
		try: 
			results = action(clientserver_socket,args,trailer) # Should not return if the action doesn't have the right number of arguments or the right types
		except TypeError:
			print "The action cannot be performed with the provided parameters"
		else:
			for r in results:
				outgoing_messages.append.(message_man.return_message(r,source))

		return outgoing_messages

		#The most basic way handle can work is it does nothing but relays so:
		# (msg, source) => (msg,other1),(msg,other2), where others = anyone who has sent a message already
