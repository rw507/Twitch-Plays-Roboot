#Author: Ryan Wrigley
#Input: List of strings that are chat message from twitch chat
#Output: The most common valid command from the list
#   Outputs null if incorrect input or no valid commands
import random

def parseChatCommands( messages ):

    #strip white space in messages and make all lower
    i = 0
    while(i < len(messages)):
        messages[i] = messages[i].lower().replace(" ", '')
        i+=1

    #build dictionary of valid commands
    commands = ["forward", "left", "right" , "back"]
    
    #for testing on twitch plays pokemon:
    commands = ["up", 'down', 'left', 'right', 'a', 'b', 'start', 'select']
    commandCounts = {}
    
    #Set count of commands to 0
    for c in commands:
        commandCounts[c] = 0
        
    #Go through messages and count frequencies of commands
    for m in messages:
        if m in commands:
            commandCounts[m] += 1

    #Find the most frequent command
    mostFrequentCommand = None
    commandFrequency = 0

    for c in commandCounts.keys():
        if(commandCounts[c] > commandFrequency):
            mostFrequentCommand = c
            commandFrequency = commandCounts[c]
    return mostFrequentCommand

class chatTracker:
        com_track =     {}
        required = 10
        def __init__(self, mode = "robot"):
                
                if(mode == "pokemon"):
                       commands = ["up", 'down', 'left', 'right', 'a', 'b', 'start', 'select']
                elif( mode == "robot"):
                        commands = ["forward", "left", "right" , "back" ]
                for c in commands:
                        self.com_track[c] = 0
               # print(self.com_track)
                        
        def pushMessage(self, m):
                m = m.lower().replace(" ", '')
                
                if( m in self.com_track.keys()):
                        m_count = self.com_track[m] + 1
                        if(m_count < self.required):
                                self.com_track[m] = m_count
                               # print m_count
                        else:
                                for k in self.com_track.keys():
                                        self.com_track[k] = 0   
                                return(m)
                else:
                        print m + " is not a valid command"
                       
        

m = ["AB C","abc", " LEFT", "RIGHT", "RiGhT"]

#print(parseChatCommands(m))


ct = chatTracker("pokemon")
commands = ["up", 'down', 'left', 'right', 'a', 'b', 'start', 'select']
for i in range(0,100):
       # print("Pushing #: " , i)
        m = ct.pushMessage(random.choice(commands))
        
        if(m):
                print(m)
