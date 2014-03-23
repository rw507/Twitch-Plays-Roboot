#Found at http://stackoverflow.com/questions/21926495/irc-bot-in-python-wont-send-messages
#Based off of Phredd's IRC bot http://pastebin.com/r1LtgEKC
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions

class twitchChatter:

	irc = socket.socket()
	spamCounter = 0
	
	channel = ''	#Channel is being set as a property 
					#because it is used in both init and messaging.
	
	def __init__(self):
		#sets variables for connection to twitch chat
		bot_owner = 'leBot'
		nick = 'lebullonwow'
		server = 'irc.twitch.tv'
		password = 'oauth:bgi56ufjkmc24jgkdpn0ktrblxpkamy'
		
		self.channel = '#lebullonwow'
		
		self.spamCounter = 0 #sets variable for anti-spam spamCounter functionality

		self.irc.connect((server, 6667)) #connects to the server
		
		#sends variables for connection to twitch chat
		self.irc.send('PASS ' + password + '\r\n')
		self.irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
		self.irc.send('NICK ' + nick + '\r\n')
		self.irc.send('JOIN ' + self.channel + '\r\n')
		
		self.spamCounterTimer()
	
	def message(self, msg): #function for sending messages to the IRC chat
		self.spamCounter = self.spamCounter + 1
		if self.spamCounter < 20: #ensures does not send >20 msgs per 30 seconds.
			self.irc.send('PRIVMSG ' + self.channel + ' :' + msg + '\r\n')
		else:
			print 'Message deleted'
	
	#Simple repeating thread for reseting the spamCounter variable.
	def spamCounterTimer(self): #function for resetting the spamCounter every 30 seconds
		self.spamCounter
		#print 'spamCounter reset'
		self.spamCounter = 0
		threading.Timer(30,self.spamCounterTimer).start()

	#This is blocking!	
	def getMessage(self):
		data = self.irc.recv(1204) #gets output from IRC server
		self.parsemsg(data)
		print data
	
		if data.find('PING') != -1:
			self.irc.send(data.replace('PING', 'PONG')) #responds to PINGS from the server
		if data.find('!test') != -1: #!test command
			self.message('Hi')
			
	#From http://stackoverflow.com/questions/930700/python-parsing-irc-messages
	#Based off of the Twisted library's irc parser.
	def parsemsg(self, s):
		"""Breaks a message from an IRC server into its prefix, command, and arguments."""
		prefix = ''
		trailing = []
		if not s:
		   raise IRCBadMessage("Empty line.")
		if s[0] == ':':
			prefix, s = s[1:].split(' ', 1)
		if s.find(' :') != -1:
			s, trailing = s.split(' :', 1)
			args = s.split()
			args.append(trailing)
		else:
			args = s.split()
		command = args.pop(0)
		return prefix, command, args

#parsemsg(":test!~test@test.com PRIVMSG #channel :Hi!")
# ('test!~test@test.com', 'PRIVMSG', ['#channel', 'Hi!'])
			
if (__name__ == "__main__"):
	myTwitchReader = twitchChatter()
	while True:
		myTwitchReader.getMessage()
	