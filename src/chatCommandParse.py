#Input: List of strings that are chat message from twitch chat
#Output: The most common valid command from the list
#   Outputs null if incorrect input or no valid commands
def parseChatCommands( messages ):

    #strip white space in messages and make all lower
    i = 0
    while(i < len(messages)):
        messages[i] = messages[i].lower().replace(" ", '')
        i+=1

    #build dictionary of valid commands
    commands = ["forward", "left", "right" , "back"]
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



m = ["AB C","abc", " LEFT", "RIGHT", "RiGhT"]

print(parseChatCommands(m))
