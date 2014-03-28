#Class definition of twitchChatter. A simple chat reader.
#This uses _settings.cfg

#TODO: Save messages to a queue.  This can later be read by the chat parser.

#Found at http://stackoverflow.com/questions/21926495/irc-bot-in-python-wont-send-messages
#Based off of Phredd's IRC bot http://pastebin.com/r1LtgEKC
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import Queue
import ConfigParser
import os

class twitchChatter:

    irc = socket.socket() #Socket for the irc chat
    spamCounter = 0       #A counter to make sure we're not spamming the irc accidentally
    config = ConfigParser.ConfigParser() #Config Settings

    def __init__(self):
    
    	self.irc.settimeout(5)

        self.config.read('_settings.cfg')
        self.server = self.config.get('ConnectionSettings', 'server')
        self.port = int(self.config.get('ConnectionSettings', 'port'))
        self.nick = self.config.get('ConnectionSettings', 'nick')
        self.password = self.config.get('ConnectionSettings', 'password')
        self.channel = self.config.get('ConnectionSettings', 'channel')

        self.spamCounter = 0 #sets variable for anti-spam spamCounter functionality

        self.irc.connect((self.server, self.port)) #connects to the server

        #sends variables for connection to twitch chat
        self.irc.send('PASS ' + self.password + '\r\n')
        #self.irc.send('USER ' + self.nick + ' 0 * :' + self.bot_owner + '\r\n')
        self.irc.send('NICK ' + self.nick + '\r\n')
        self.irc.send('JOIN ' + self.channel + '\r\n')

        self.spamCounterTimer()

    #Send a message to the irc chat
    def message(self, msg):
        self.spamCounter = self.spamCounter + 1
        if self.spamCounter < 20: #ensures does not send >20 msgs per 30 seconds.
            self.irc.send('PRIVMSG ' + self.channel + ' :' + msg + '\r\n')
        else:
            print 'Message deleted'

    #This is blocking!  Returns the next message said in the chat
    def getMessage(self):
    
    	returnMessage = ("", "")
    
        data = self.irc.recv(1204) #gets output from IRC server
        inMessage = self.parsemsg(data)

        #This try will print out any chat messages.  Otherwise, it just prints data.
        try:
            #Actual chat messages go through here.
            if(len(inMessage) > 2):
            	returnMessage = (inMessage[0].split('!')[0], inMessage[2][1]) #username, message
        except IndexError:
        	pass
            #print data

        if data.find('PING') != -1:
            self.irc.send(data.replace('PING', 'PONG')) #responds to PINGS from the server
        if data.find('!test') != -1: #!test command
            self.message('Hi')
            
        return returnMessage

    #From http://stackoverflow.com/questions/930700/python-parsing-irc-messages
    #Based off of the Twisted library's irc parser.
    def parsemsg(self, s):
        """Breaks a message from an IRC server into its prefix, command, and arguments."""
        prefix = ''
        trailing = []
        if not s:
            #raise IRCBadMessage("Empty line.")
            pass
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

    #Simple repeating thread for reseting the spamCounter variable every 30 seconds.
    def spamCounterTimer(self):
        self.spamCounter = 0
        threading.Timer(2,self.spamCounterTimer).start()

    #TODO
    def setConfigSetting(self, section, key, value):
        pass

    def saveConfigSettings(self):
        pass

    def getMessageFromQueue(self):
        pass

    def purgeQueue(self):
        pass

#Unit Test
if (__name__ == "__main__"):
    myTwitchReader = twitchChatter()
    while True:
        print(myTwitchReader.getMessage())

