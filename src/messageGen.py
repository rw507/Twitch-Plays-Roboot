import random

class messageGen:

	startMessages = [
		"Don't worry, I'm here!",
		"I'm ready now!",
		"Hello, humans!",
		"Hello, people!"
	]

	boredMessages = [
		"Hello?",
		"Is anyone there?",
		"I really want to play! Where are you?",
		"Guys, this isn't funny!",
		"Is this a trick?  I don't like it.",
		"Is somebody out there?",
		"Please someone talk to me!",
		"Please come back and play with me!"		
	]
	
	encouragingMessages = [
		"Let's do this!",
		"We can do it!",
		"We're doing it!",
		"Come on guys, lets roll!"
	]
	
	moveVerbs = [
		"Going",
		"Moving",
		"Executing",
		"Traveling"
	]
	
	turnVerbs = [
		"Executing",
		"Turning",
		"Rotating",
		"Yawing"
	]
	
	def getStartMessage(self):
		return random.choice(self.startMessages)
	
	def getBoredMessage(self):
		return random.choice(self.boredMessages)
	
	def getMoveMessage(self, command):
		moveVerb = random.choice(self.moveVerbs)
		return moveVerb + " " + str(command) + "."
		
	def getTurnMessage(self, command):
		turnVerb = random.choice(self.turnVerbs)
		return turnVerb + " " + str(command) + "."

if (__name__ == "__main__"):
	myMessenger = messageGen()
	print myMessenger.getStartMessage()
	print myMessenger.getBoredMessage()
	print myMessenger.getMoveMessage("up")
	print myMessenger.getTurnMessage("left")
		
		