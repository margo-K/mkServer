# @@ mkServer.py Module @@
## Provides classes, methods and variables for creating, maintaining and closing down a working IRC serverS


import socket
import select
import sys
import threading
import Queue
import time





class Server: 
	"""A class for creating a home server that will operate an IRC chat
	* Creates a 'listen' port for the user 
	* Accepts incoming connection requests from clients desiring connection 
	* Receives messages from clients & queues them (based on time received)
	* Sends the messages out to all users ** (BRANCH: to all users on that channel, to individuals)
	* Shuts down after a certain period of inactivity
	""" 

	#State Changing
	def __init__ (self):
		"""Create all class-level attributes"""
		self.current_sockets = []
		self.message_queue = Queue.Queue()
		self.username_directory = {}  #keys = socket objects, entries = usernames
		self.action_dictionary = {"/NICK": self._store_username, "/EXIT": self._client_terminate, "/MSG": self._ping}
		self.message_rest = {} # keys = clientserver_sockets

	#State Changing
	def _create_serversocket(self):
		"""Create a new listening server socket"""
		self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
		self.server_socket.setblocking(0) #non-blocking
		self.server_socket.bind((host,port))
		self.server_socket.listen(5)

		print "Listening at", self.server_socket.getsockname()
		
	def server_setup(self,host,port):
		"""Create the server and initialize the readlist"""
		self._create_serversocket()
		self.current_sockets.append(self.server_socket) # initializes readlist

	# _client_accept :: (<accept()>)=>new cs_socket ::  (<function>)=> Socket
	def _client_accept(self): 
		"""Accept a new client"""
		clientserver_socket, clientserver_address = self.server_socket.accept() #where addr :: the address bound to the socket on the other end of the connection
		print "Connection from: ", clientserver_address
		print "Socket connects", clientserver_socket.getsockname(), "on the server side to", clientserver_socket.getpeername(), "on the client side."
		return clientserver_socket

	#State Changing
	def _store_username(self,clientserver_socket,username):
		"""Store a client's username in the username dictionary"""
		self.username_directory[clientserver_socket] = username
		print username + "has been stored as a username." 

	#State Changing
	def setup_user(self):
		"""Accept a new client and get them set up for communication"""
		new_socket = self._client_accept()
		new_socket.setblocking(0) # non-blocking
		self.current_sockets.append(new_socket)
		self.message_rest[new_socket] = ''
	

	# Pure: <message,clientserver_socket> => formatted message :: <String,socketobject> => String
	def _message_maker (self,clientserver_socket,message):
		"""Format a message so that it includes the username; Used as message is sent"""
		username = self.username_directory[clientserver_socket]
		return "%s: %s \n" %(username,message)

	#Pure
	def _decode_data(self, lump):
		"""Return two values: list of parsed messages () and a string of partial data"""
		splits = lump.split('\n')
		msgs = splits[:-1]
		rest = splits[-1]
		return [self._parse_message(m) for m in msgs], rest

	# Pure: <self,String,Socket> -> (action :: function, argument :: String), Boolean | message :: String, Boolean""
	def _parse_message(self,message):
		"""Return a tuple including the method for action being performed and the argument it accepts"""
		print "The message being parsed is " + str(message) + "\r"
		print "It is " + str(message.startswith('/'))+ "that the message starts with a /"
		# try:
		if message.startswith('/'):
			(tag,delimiter,argument) = message.partition(' ') # Splits the action call off from the argument
			action = self.action_dictionary[tag]
			return (action,argument)
		# else: 
		# 	return error

	# 	message_triage :: !return
	# 	message_triage calls :: self._parse_message() | self._client_terminate()
	# 	message_triage alters :: (optionally) self.message_queue + that which is altered by - <action>, _parse_message(), _client_terminate()
	
	def _ping(self,clientserver_socket,message):
		"""Called when a message is sent from the clientserver_socket"""
		self.message_queue.put((message,clientserver_socket))

	def message_process(self,clientserver_socket):
		"""Receives messages and performs the requested action, which always involves a state-change"""
		received = self.message_rest[clientserver_socket] + clientserver_socket.recv(1024)
		sndr_addr = clientserver_socket.getpeername() 
		print  "%s: says %s."% (sndr_addr,received)

		if received == '': # Connection has failed
			self._client_terminate(clientserver_socket, " Closing %s after reading no data"%sndr_addr)
		else: 
			messages, rest = self._decode_data(received) #Note: the problem right now is that decode_messages returns a string of messages and the methods below operate on a single one
			for m in messages:
				action, argument = m
				print "This is the action: " + str(action)
				print "This is the argument: " + str(argument)
				action(clientserver_socket,argument)

			self.message_rest[clientserver_socket] = rest	
			
	def _client_terminate(self,clientserver_socket,exit_message = "Client Exiting"):
		addr = clientserver_socket.getpeername()
		usn = self.username_directory[clientserver_socket]
		self.current_sockets.remove(clientserver_socket)

		clientserver_socket.close()
		print (exit_message + "Client %s Removed at %s") % (usn,addr)

	def daily_activity(self):
		""" Perform the accepting of new clients, receiving of new messages and the distribution of the messages """
		
		read_result, write_result, error_result = select.select(self.current_sockets, self.current_sockets, self.current_sockets) #Does this formulation allow them to change?
		
		for socket in read_result: # any socket
			#Checks to see if the "msg" is a client wanting to connect
			if socket is self.server_socket:
				self.setup_user()
			#Else, Listens for messages from clients
			else:
				self.message_process(socket)

		try:
			message,sender = self.message_queue.get_nowait()
		except Queue.Empty:
			pass
			#write_try.remove(socket) #Does this makes sense? Do i want to remove someone from the write list if they're not sending messages?? I don't think so
		else:
	 		for sckt in write_result:
	 			if sender is not sckt:
	 				current_message = self._message_maker(sender,message)
		 			print 'Sending "%s" to %s' % (current_message,socket.getpeername()) 
		 			sckt.send(current_message)

	# def server_terminate(self):
	# 	"""Closes the server socket"""
	# 	self.server_socket.close() # closes the server socket
    

class Client:
	"""A class creating client-associated sockets and interacting with users of a basic IRC server. Does the following:
	* allocates incoming and outgoing ports for them
	* connects these ports to the given server, with which it is interacting
	* Allows user to input a username, to be stored and referred to
	* Stores the user's input from keystrokes and sends them to the server
	* Provides an exit option for the user, allowing them to initiate the process of closing their socket"""

 		
	def _create_socket(self):
		"""Create new client socket."""
		self.socket = socket.socket() 
		#self.socket.setblocking(0)

	def _connect_client(self,host,port):# fucked, needs to be refactored
		"""Connect socket to server."""
		return_value = self.socket.connect((host,port)) # useful for testing
		if return_value:
			return return_value

	def _set_threading_default(self):
		self.keepthreadin = True # Do I want it set to true or false, initially? do i want to declare this now?

	def _store_address(self):
		"""Store socket address in a local variable."""
		self.address = self.socket.getsockname() # All addresses are stored upon creation - do we ever need one part alone?
		
		print 'Client has been assigned socket name', self.address

	def client_setup(self,host,port):
		"""Initiate a client connected to the server."""
		self._create_socket()
		self._connect_client(host,port)
		self._set_threading_default()
		self._store_address()



	def _prompt_username(self):
		"""Prompt for username and store value."""
		self.username = raw_input("Please enter your username: ")

	def _send_username(self):
		"""Send the username to the server."""
		message = "/NICK " + self.username
		print "The message at the username step is" + str(message)
		self.socket.send(message)
	
	def _get_username(self):
		"""Get the client's username and send it to the server."""
		self._prompt_username()
		self._send_username()
		print "I got the username"


	def _send_messages(self):
		"""Accept messages from the client and send them to the server."""
		while self.keepthreadin == True:	
			message = raw_input("Please enter a message: ") 
			packet = "/MSG " + message 
			print "Here's a packet being sent, if you dare: " + packet
			self.socket.send(packet) 


	def _receive_messages(self):
		"""Receive messages from the server and print them to the console."""
		while self.keepthreadin == True:
			self.socket.recv(1024)
			#print reply

	def initiate_communication(self):
		"""Create threaded message inbox and outbox."""
		#while self.keepthreadin = True:
		self.outbox = threading.Thread(target=self._send_messages)
		print "I made the inbox"
		self.outbox.daemon = True
		self.inbox = threading.Thread(target=self._receive_messages)
		print " I made the outbox"
		self.inbox.daemon = True
		self.inbox.start()
		self.outbox.start()

	#What are my assumptions:
		#1. start just means the action gets performed in that thread
		#2. the action gets performed for each time it has an input (for send messages this would be each time i receive something from raw_input; for receive_messages, for each time that i actually have a message waiting )
		#3. that the actions just wait 
	#Will not be employed in the Client script, only in the Server script on client objects
	def user_exit (self,exitBool_client):
		"""Stop all user activity and shutdown communication on the user end. Used only by the server."""
		if exitBool_client == True:
			self.keepthreadin = False # Terminates the threads for accepting/receiving
			self.shutdown(socket.SHUT_WR) #Allows the server to still send remaining messages while signaling that it is shutting down its own write capabalities
		# Options are: SHUT_WR (further sends disallowed), SHUT_RD (further reads disallowed), SHUT_RDWR(both disallowed);
		#Note: some OS's make shutting down one half of the connection also close the opposite half (supposedly on OSX, shutdown(SHUT_WR) does not allow further reads on the other half)
		#Question: does doing one half or the other cause problems - for example for the closing/opening messages send by TCP?
		#If exitBool_c == True, the socket's WR capability is shutdown. Note: exitBool_c can be set to True or it can take an expression to be evaluated
# class ClientServerSocket(#Socket: doesn't need to inherit cause it's not a socket object - it's an object that CONTAINS a socket object, and several other things. Also, the socket methods are inhereted from the import):
# 	"""This Entity will have the following characteristics:
# 	Attributes: 
# 		username:
# 		address:
# 		socket object: passed in as a parameter for the init




if __name__== '__main__':
	host = '127.0.0.1' # Allows only local folks to connect
	port = 1060 # A randomly chosen port for listening

	if sys.argv[1] == 'client':
	    c = Client()
	    c.client_setup(host,port)
	    c._get_username()
	    c.initiate_communication() # employs the send_messages and recv_messages methods

	if sys.argv[1] == 'server':
	    s = Server()
	    s.server_setup(host,port)

	    while True: #len(s.read_try)> 1 : # there are users other than the server
	    	s.daily_activity()#Goes about the process of accepting clients, getting communication going and closing their sockets, if necessary or requested

	    s.server_terminate()
	    #s.server_terminate() --- you need to do this sequentially, cause you don't want it to terminate before the client has a chance to connect
   #The actual closing part will happen on the part of the server


# USE THIS: * i.e. args = [3,6]; range(*args) >> [3,4,5]



