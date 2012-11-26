# @@ test_mkserver.py
#Provides for Unit Testing on the individual functions of the mkServer.py class
#Created by Margo Kulkarni

import socket
import unittest
import Queue
from mkServer import Server, Client


class FakeSocket():

	def accept(self):
		return "Socket", ("1.1.1.1.1",0)

	def send(self,message):
		return True

	def recv(self,length):
		return "Message"

	def getsockname(self):
		return host,port

	def bind(self,(host,port)):
		return True

	def connect(self,(host,port)):
		return True

	def listen(self,number):
		return True

	def setblocking(self,blockboolean):
		if blockboolean == 0:
			return True
		else:
			return False


class MkServer_Server_Tests (unittest.TestCase):
	""" Check whether all of the functions that involve qualities of the Server's (listen socket, etc.).
		One of the primary tests involves creating two objects from state_level_setup and comparing all 
		the state variables of the newly instantiated one to the state variables of one which has gone
		through the method (cause that enables you to identify the side effects)  """

	def state_level_setup(self):
		"""This sets up a server with all the state level variables instantiated at once"""

	def 

	def test_create_serversocket(self):		
		"""Checks that a new server socket has been created"""
		server = Server()
		server._create_serversocket()

		self.assertIsInstance(server.server_socket,socket.socket)


	def test_socket_setup(self):
		"""Checks to see whether the socket is now listening"""

		#Create a new instance of a test_server
		server = Server()
		server.server_socket = FakeSocket()

		#Executes the function to be tested
	
		#Checks whether the server_socket is listening
		self.assertTrue(server._socket_setup(host,port))

	def test_initialize_readlist(self):
		""" Checks whether the server is in the read list"""

		#Creates a new instance of the test_server
		server = Server()
		server.server_socket = "Socket"

		#Executes the function to be tested
		server._initialize_readlist()

		#Checks that the socket is in the readtry list
		self.assertIn("Socket",server.read_try)


#class MKServer_Queue_Tests (unittest.TestCase):

	# def setup_queues(self):
	# 	""" Sets up a new client with an empty message queue"""
	# 	self.trial_server = mkServer.Server(host,port)
	# 	self.trial_server.read_try = [trial_server.server_socket] # Needs to be a fake socket
	# 	self.trial_server.message_queues[dummy_cs_socket] = Queue.Queue() #Creates a new queue with the dict key as the dummy socket

#Question: does this "selfing" cause trouble? Should it return these things instead



	def test_addto_readlist(self):
		"""Checks whether the input socket has been added to readlist after the method is called"""

		#Creates a test server and assigns a fake socket to its socket value
		server = Server()
		sock = "Socket"

		#Tries the method
		server._addto_readlist(sock)

		#Checks whether the socket appears in the readlist 
		self.assertIn(sock,server.read_try)
	

	"""These are all the tests for the messaging functionality"""

	# def test_is_action(self):
	# 	"""Given an input string starting with "/", it checks whether is_action evaluates to true """
		
	# 	server = Server()
	# 	message = "/Action"

	# 	#Tries the function
	# 	result = server.is_action(message) ##### NEEEDS A SERVER OBJECT TO OPERATE ON .. OUR MESSAGE NEEDS TO BE A CLASS
		
	# 	#Checks if it asserts to true
	# 	self.assertTrue(result)

	#Question: What do you actually need for this test? 1. a message dictionary and corresponding queue, setup the way you would (though if you test this elsewhere, then maybe not) 2. a key for the dictionary - but really it doesn't need to be a socket 3. a message - anything - to check for; could even be a boolean ?
	def test_add_message(self):
		"""Checks whether a new message actually appears in the Queue after message_accept has been called on it"""
		#server = Server(host,port)
		#client = Client() / doesn't actually need a new client because all you care about is the message queue
		#client.add_username() # n
		server = Server() # Sets up the queue for usage
		socket = 'Socket' # Does not actually need to have socket qualities
		server.message_queues[socket]=Queue.Queue()
		message = 'Test'

		#Executes the function being tested
		server._add_message(socket,message) # Calls message_accept method on the test message

		#Checks whether the message now appears in the Queue
		result = server.message_queues[socket].get() # Gets the first element in the queue. 
		self.assertEquals(message,result) # Checks if it's equal to the other one

	#Question: What do you actually need for this test?:
	# 1. A write_list to add to (just an empty list) - unless the list can get full - any other errors?
	# 2. a cs_socket - with no qualities other than existing
	# 3. Probably needs to have a client, cause you want to know if it happens to the global version of this - or at least needs to have acces to a dummy version of a global list created elsewhere and part of the same class
	def test_addto_writelist(self):
		""" Checks whether addto_writelist actually adds the input to the writelist"""
		
		#Creates the trial server instance
		server = Server() # Note: because socket setup is done elsewhere, you don't actually need to worry about that. The init just has a bunhc of empty lists and dictionaries

		#Tries the actual addto_writelist method
		server._addto_writelist("Socket")

		self.assertIn("Socket",server.write_try)

		#Question: What happens is the list is empty?



#Tests that have to do with client-server sockets:
	def test_client_accept(self):
		"""Checks whether the attempt to a accept a new client was successful by returning the new socket object and address created on the server side"""

		#Creates a new server and makes its server_socket a fake socket
		server = Server()
		server.server_socket = FakeSocket()

		#Tests the method using that new fake server_socket - but how do we do this 
		self.assertEquals(server._client_accept(), "Socket")



#Tests that have to do with lookup to the dictionary or messages (including message queues):

#Need to know that the object you're asking for already exists in the dictionary, which you would know if you had all things being added to the dictionary at the same time
#Test: If there is an entry in the dictionary for that person, the function will return a string with their username and a colon appended to the message	
	
	def test_setto_nonblocking(self):
		"""Check that the nonblocking option has been set"""
		server = Server()
		socket = FakeSocket()

		self.assertTrue(server._setto_nonblocking(socket))

	def test_allocate_message_queue(self):
		"""Check that a message queue has been allocated for the given new connection"""

		server = Server()

		self.assertEquals(server.message_queues,{})

		server._allocate_message_queue("socket")
		self.assertIsInstance(server.message_queues["socket"],Queue.Queue)




		#Calls the method

		#Then checks to see what is returned from the dictionary for that fake socket, specifically it checks if a queue is returned

	# def test_get_username(self):
	# 	"""Check that"""
	# 	server = Server()
	# 	#server.username_dictionary["Socket"] = "username"

	# 	print "Don't forget about testing me:" + "_get_username"
	# 	#self.assertself.server.username_dictionary[]

	# 	pass 

	def test_store_username(self):
		"""Check that the client has a username in the dictionary only after method call"""

		server = Server()
		new_socket = "Socket"
		username = "User's Name"

		self.assertTrue(new_socket not in server.username_dictionary)

		server._store_username(new_socket,username)

		self.assertEquals(server.username_dictionary[new_socket],username)


	
	def test_message_maker(self):
		"""Check whether the output is a string and whether it matches the message format"""
		server = Server()

		result = server._message_maker("message","username") 

		#Checks to see if the function does what it's supposed to
		self.assertIsInstance(result,str)
		self.assertEquals("username: message",result)

	def test_is_connected(self):
		"""Check that a client_server socket is still connected to  its pair on the client side"""
		pass

class MKServer_Client_Tests(unittest.TestCase):

	def setUp(self):
		"""Creates an instance of the client so that tests can be run"""
		self.client = Client() #This intialization doesn't actually do anything..
		self.client.socket = FakeSocket()
 

		#Do we need to do the fake_client_setup here? We definitely need a socket by the time we get to store_address
	def test_create_socket(self):
		"""Tests whether the socket attribute now contains a socket object"""

		self.client._create_socket()

		self.assertIsInstance(self.client.socket, socket.socket)

	def test_connect_client(self):
		"""Check that the socket is connected."""
		confirmation = self.client._connect_client(host,port)

		self.assertTrue(confirmation)

		#Calls the setup method (this is the init, so no other init is needed):

	def test_store_address(self):
		"""Check that address value is not null."""
		#Needs: a faux client to operate on (done in the setup..?)

		# Runs the function
		#self.assertFalse(hasattr(self.client, 'address') # Interesting - this field doesn't exit until now, so this is an error?
		self.client._store_address()

		self.assertIsNotNone(self.client.address)

#Decided not to test this because it would just be testing whether raw_input works - but maybe whether it's blocking
	# def test_prompt_username(self):
	# 	"""Checks whether the function outputs what came in from raw input"""
	# 	#Needs: faux raw input

	# 	#Calls the function
	# 	result = self.client._prompt_username()

	# 	self.assertEquals(self.faux_rawinput,result) # NEeed to define faux_raw input somewhere and make that the input for the function


	#How do I fix this?!
	def test_send_username(self):
		"""Checks whether the username from raw input has been received by the server socket"""
		#Needs: Server Socket (or replica), something for raw input & a client to call the method
		self.client.username = "Name"
		self.assertTrue(self.client._send_username())


	####BOTH OF THE BELOW ARE DIFFICULT TO TEST BECAUSE OF THE THREADS - SHOULD I TEST THE WHILES OR WHAT
		pass

	def test_receive_messages(self):
		""""""
		pass 

	def test_initiate_communication(self):
		pass

	def test_user_exit(self):
		pass 






#Tests Functions Outside of Both
	


	
# #Tests Server Functions
# 	def test_init_sockname():
# 		"""The function should test whether the servsock.getsockname() returns the same as whatever it was bound to """
# 	def test_clientEnd():
# 		"""The function should close the client socket requesting closure and remove it from the list.
# 		The test checks whether the client is still on the list & whether sending a message to/from the client does anything """
# 				#Under what circumstance might the client still be on the list?
# 	def test_daily_activity_wrelist():
# 		"""The function tests whether the readlist, writelist and errorlist are getting properly updated"""
# 	def test_daily_activity_writeable():
# 		"""Tests whether all users are getting the messages (i.e. appearing as writeable & being written to), returns an error if some are having issues"""
# #Tests Client Functions
	



# 	def test_addUsername():
# 		""" The function should prompt the user for a username and input it into the dictionary
# 		The test checks whether 1) The proper exception/error message is thrown if there's no input
# 		2) and whether the username does indeed appear in the dictionary
# 		3) whether the username has been changed from "" after the function """

# 	def test_send_message():
# 		""" """
	
# 	def test_user_exit():
# 		"""The function's purpose is to signal to the server that the user has decided to exit, 
# 		So the test checks whether the server can still send/receive messages to/from the client and checks whether the server. It also checks whether the client can still send/receive messages."""

# 	def test_user_exit_threadexit():
# 		""" Checks whether an 'exit' on the receiving end of one thread results in both threads being ended & the socket closed"""
# 		for 
# 		thread.is_alive() 
# #Other stuff:

# 	def test_addr of client():
# 		"""Checks whether addr in accept fn matches what the server self-identifies as in getsockname()"""

# 	def test_socket_connect():
# 		"""Checks if the socket is actually conencted"""
#Executes the tests
if __name__ == '__main__':
	unittest.main()

