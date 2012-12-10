# @@ mkServer.py Module @@
## Provides classes, methods and variables for creating, maintaining and closing down a working IRC serverS

import socket
import select
import Queue
from brain import Brain
from ircparts import Channel, User, Message



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
		self.message_queues = {} # keys = sockets, entries = outgoing message queue for that user
		self.message_rest = {} # keys = clientserver_sockets
		self.mind = Brain()
	
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
		"""* Accept a new client"""
		clientserver_socket, clientserver_address = self.server_socket.accept() #where addr :: the address bound to the socket on the other end of the connection
		print "Connection from: ", clientserver_address
		print "Socket connects", clientserver_socket.getsockname(), "on the server side to", clientserver_socket.getpeername(), "on the client side."
		return clientserver_socket

	#State Changing
	def setup_user(self):
		"""* Accept a new client and get them set up for communication"""
		new_socket = self._client_accept()
		new_socket.setblocking(0) # non-blocking
		self.current_sockets.append(new_socket)
		self.message_rest[new_socket] = ''
		self.message_queues[new_socket] = Queue.Queue()
	#Pure
	def _decode_data(self, lump):
		"""Return two values: list of parsed messages () and a string of partial data"""
		splits = lump.split('\n')
		msgs = splits[:-1]
		rest = splits[-1]
		return msgs, rest

	def message_process(self,source_socket):
		""" * Receives messages and performs the requested action, which always involves a state-change

		WHAT IT SHOULD DO: 
			- send each message to the brain to be parsed and dealt with
			- receive messages from the brain and enqueue them in the necessary queues
		"""
		received = source_socket.recv(1024)
		sndr_addr = source_socket.getpeername() 
		print  "%s: says %s"% (sndr_addr,received)

		if received == '': # Connection has failed
			self._client_terminate(source_socket, " Closing %s after reading no data"%sndr_addr)
		else:
			messages, new_rest = self._decode_data(self.message_rest[source_socket] + received) #Note: the problem right now is that decode_messages returns a string of messages and the methods below operate on a single one
			print "The message is %s and the rest is %s"%(messages,new_rest)
			self.message_rest[source_socket] = new_rest

			for m in messages:
				responses = self.mind.process(m,source_socket) # returns messages that must be sent out as a result of the requested action

			for response in responses:
				content,destination = response
				print "I'm about to put the message %s in %s's queue"%(content,destination)
				self.message_queues[destination].put(content)

	def daily_activity(self):
		"""  Perform the accepting of new clients, receiving of new messages and the distribution of the messages """
		
		read_result, write_result, error_result = select.select(self.current_sockets, self.current_sockets, self.current_sockets) #Does this formulation allow them to change?
		
		for socket in read_result: # any socket
			#Checks to see if the "msg" is a client wanting to connect
			if socket is self.server_socket:
				self.setup_user()
			#Else, goes through the process of reading messages and sending them to the brain to be processed
			else:
				self.message_process(socket)

		# subtle bug: if someone isn't in the write_result list, they will miss the message
		
		for socket in write_result:
			try:
				message = self.message_queues[socket].get_nowait()
			except Queue.Empty:
				pass
			else:
			 	print 'Sending "%s" to %s' % (message,socket.getpeername()) 
	 			socket.send(message)

	def server_terminate(self):
		"""Closes the server socket"""
		self.server_socket.close() # closes the server socket
 

if __name__== '__main__':
	host = '127.0.0.1' # Allows only local folks to connect
	port = 1060 # A randomly chosen port for listening

	s = Server()
	s.server_setup(host,port)

	try: #len(s.read_try)> 1 : # there are users other than the server
		while True:
			s.daily_activity()#Goes about the process of accepting clients, getting communication going and closing their sockets, if necessary or requested
	except KeyboardInterrupt:
		print "\n The server will now exit"
		s.server_terminate()

