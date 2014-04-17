import sys
import threading
import time
from twitchChatter import *


class chatterParser(threading.Thread):
  lock = threading.Lock()
  count = 0
  commands = ["up" , "left", "right"]   
  
  def __init__(self, threshold ):
    threading.Thread.__init__(self)
    self.threshold = threshold
    self.twitchReader = twitchChatter()
    self.reset()
    self.running = True   
  
  def stop(self):
    self.running = False
  
  def getCommand(self):
    pass
  
  def run(self):
    while(self.running):      
      message = self.twitchReader.getMessage()
      if(message[0].strip() == "" or self.nextCommand):
	continue
      if(message[0] == "Twitch_plays_robot"):
	self.nextCommand = message[1]
	continue
      clean = self.cleanMessage(message[1])     
     # print("Is " + clean + " a command?")
      if clean in self.commands:
	#print("yes")
	with self.lock:
	  self.comCount[clean]+=1
	  if(self.comCount[clean] >= self.threshold):
	    self.nextCommand = clean

	
	
  def cleanMessage(self, raw):
    clean = raw.lower().replace(" ", "").strip()
    return clean
  
  def reset(self):   
    with self.lock: 
      #print("Restarting...")
      #print("Original Count: " + str(self.count))
      
      self.count = 0
      self.nextCommand = None      
      self.comCount = {}
      for c in self.commands:
	self.comCount[c] = 0
      #print("This should be 0: " + str(self.count))
  def getNextCommand(self):
    if(self.nextCommand):
      c = self.nextCommand
      self.reset()
    else:
      return None
    
    return c
  def stop(self):
    self.running = False 
    
      
  
if __name__ == ("__main__"):
  threshold = 2
  chatterParser = chatterParser(threshold)
  chatterParser.start()
  
  for i in range(100):
    time.sleep(1)
    print(chatterParser.getNextCommand())
    
  chatterParser.stop()
  
  """
  time.sleep(2) 
  chatterParser.reset()
  time.sleep(2)
  print("STOPPING!!!")
  chatterParser.stop()
  """
  