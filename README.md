#mKay Server
An IRC Server with basic functionality, written in python from sockets up

###Contents
- __mkServer.py__ : Handles all outgoing & incoming messages along TCP sockets
- brain.py : Forms the link between the irc protocol and the TCP-based server. Acts as the "mailman" for the incoming messages, sending each message to the parties (below) which are affected by it.
- ircparts.py module : Comprises the objects being created, altered and destroyed through IRC commands
	1. Message_Manager
	2. Message
	3. Channel
	4. User

###Getting Started
#####Open REPL

Start the server locally on port 1060:
```
python mkServer.py
```

Quit the server with keyboard interrupt

###Tests
Currently, the only working tests are those in parser_test.py, which just test the function which parses IRC message strings into its components

###Status

Currently, the outer-most layer (mkServer.py) has its complete functionality implemented. All other files are works-in-progress.

###Supported IRC Functionality
Drawn from the original Internet Relay Chat Protocol ([RFC 1459, 1993](http://www.irchelp.org/irchelp/rfc/rfc.html)) & a non-standard update, Internet Relay Chat: Client Protocol ([RFC 2812, 2000](http://tools.ietf.org/html/rfc2812))

- NICK : setting a nickname
- USER : setting the user (necessary for initial connection)
- MODE (user only)
- PRIVMSG : messaging individual users and channels
- JOIN, PART : joining and leaving a chatroom 
- QUIT : disconnecting from a server

###Notes
mkClient.py & test_mkServer.py are from an older version of the program and do not currently function with the present form