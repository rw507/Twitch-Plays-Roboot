import random



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

def getStartMessage():
	return random.choice(startMessages)

def getBoredMessage():
	return random.choice(boredMessages)

def getMoveMessage(command):
	moveVerb = random.choice(moveVerbs)
	return moveVerb + " " + str(command) + "."
	
def getTurnMessage(command):
	turnVerb = random.choice(turnVerbs)
	return turnVerb + " " + str(command) + "."

if (__name__ == "__main__"):
	myMessenger = messageGen()
	print myMessenger.getStartMessage()
	print myMessenger.getBoredMessage()
	print myMessenger.getMoveMessage("up")
	print myMessenger.getTurnMessage("left")
		
		