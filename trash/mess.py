from twitchChatter import *
import os

#Unit Test
if (__name__ == "__main__"):
    myTwitchReader = twitchChatter()
    
    cmdMap = {}
    cmdMap['up'] = 'w'
    cmdMap['down'] = 's'
    cmdMap['left'] = 'a'
    cmdMap['right'] = 'd'
        
    while True:
		message = myTwitchReader.getMessage()
        
		chatCmd = message[1].replace("\r\n", "")
        
		if chatCmd in cmdMap.keys():
			cmd ="osascript -e 'tell Isaac \"System Events\" to keystroke " + cmdMap[chatCmd] + "' "
			# minimize active window
			os.system(cmd)
        