import socket
import threading
import ircexceptions

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
	c = Client()
	c.client_setup(host,port)
	c._get_username()
	c.initiate_communication() # employs the send_messages and recv_messages methods

