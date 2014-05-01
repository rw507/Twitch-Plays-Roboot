#Class definition of twitchChatter. A simple chat reader.
#This uses _settings.cfg

#TODO: Save messages to a queue.  Block if the queue is empty.

#Found at http://stackoverflow.com/questions/21926495/irc-bot-in-python-wont-send-messages
#Based off of Phredd's IRC bot http://pastebin.com/r1LtgEKC
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import Queue
import ConfigParser
import os
import time

class twitchChatter:

    irc = socket.socket() #Socket for the irc chat
    spamCounter = 0       #A counter to make sure we're not spamming the irc accidentally
    #config = ConfigParser.ConfigParser() #Config Settings
    lastMessage = ("", "")
    messageQueue = Queue.Queue()
    messageCount = 0

    def __init__(self):

        self.irc.settimeout(5)

        #self.server = "199.9.252.26"
	self.server = "irc.twitch.tv"
        self.port = 6667
        self.nick = "Twitch_Plays_Robot"
        self.password = "oauth:4yacpxm65x6gb71jv91zvyo3npf0qzt"

        #self.channel =  "#twitchplayspokemon"
	self.channel = "#twitch_plays_robot"

        self.spamCounter = 0 #sets variable for anti-spam spamCounter functionality

        self.irc.connect((self.server, self.port)) #connects to the server
	self.irc.settimeout(None)

        #sends variables for connection to twitch chat
        self.irc.send('PASS ' + self.password + '\r\n')
        self.irc.send('NICK ' + self.nick + '\r\n')
        self.irc.send('JOIN ' + self.channel + '\r\n')

        self.spamCounterTimer()

        self.readerThread = threading.Thread(target = self.readMessages)
        self.readerThread.setDaemon(True)
        self.readerThread.start()


    #Send a message to the irc chat
    def sendMessage(self, msg):
        self.spamCounter = self.spamCounter + 1
        if self.spamCounter < 20: #ensures does not send >20 msgs per 30 seconds.
            self.irc.send('PRIVMSG ' + self.channel + ' :' + msg + '\r\n')
        else:
            print 'Message deleted'
            
    #This is blocking!  Returns the next message said in the chat
    def getMessage(self):        
        return self.messageQueue.get()
        

    

    def readMessages(self):

        while(True):
            data = self.irc.recv(1204) #gets output from IRC server
            inMessage = self.parsemsg(data)
            
            #Actual chat messages go through here.
            if(len(inMessage[2]) >= 2):
                self.messageQueue.put((inMessage[0].split('!')[0], inMessage[2][1])) #username, message


            """
            if data.find('PING') != -1:
                    self.irc.send(data.replace('PING', 'PONG')) #responds to PINGS from the server
            if data.find('!test') != -1: #!test command
                    self.sendMessage('Hi')
            """



        

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

#Unit Test
if (__name__ == "__main__"):

    
    
    myTwitchReader = twitchChatter()
    print("hi");
    while True:
       
        print(myTwitchReader.getMessage())
        time.sleep(1)

