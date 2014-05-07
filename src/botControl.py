#!/usr/bin/env python

import rospy
from geometry_msgs.msg import *
from sensor_msgs.msg import *

import time
import re

import signal
import sys

from chatterParser import chatterParser
import messageGen
obstacle_near = False

#Handle signals
def handler(signum, frame):
	print 'Here you go'
	exit(0)

def laserCallback(data):
	global obstacle_near

	obstacle_distance_threshold = 1.0

	#print 'Got new laser scan at ', rospy.Time.now()
	min_range = data.range_max
	for i in range(len(data.ranges)):
		if data.ranges[i] < min_range:
			min_range = data.ranges[i]

	#print 'Minimum range from scan is : ', min_range
	if min_range < obstacle_distance_threshold:
		obstacle_near = True
	else:
		obstacle_near = False


#General movement Function
def move(inDir, maxTicks, checkForObsticals = True):
	global twist
	global obstacle_near
	
	tick = 0
	
	while(tick < maxTicks):
		tick += 1
		rospy.sleep(0.1)
		#time.sleep(0.1)
		
		if(checkForObsticals and obstacle_near):
			avoidObstical()
			break
			
		twist.linear.x = inDir[0]
		twist.angular.z = inDir[1]
		
		pub.publish(twist)

#Moves to make if we run into an obstacle	
def avoidObstical():
	move((-1, 0), 10, False)
	move((0, 1), 10, False)

	

#Main Loop
if __name__ == '__main__':
	rospy.init_node('bouncer', anonymous=True)
	pub = rospy.Publisher('cmd_vel', Twist)
	pub = rospy.Publisher('/moble_base/commands/velocitys', Twist)
	rospy.Subscriber("base_scan", LaserScan, laserCallback) 
	
	twist = Twist()
	
	chatterParser = chatterParser(1)
	chatterParser.start()
	myTwitchChatter = chatterParser.getTwitchChatter()

	myTwitchChatter.sendMessage(messageGen.getStartMessage())

	timeoutCounter = 0
	while(True):
		#Timeout
		if(timeoutCounter > 10000):
			nextCommand = chatterParser.forceNextCommand()
			timeoutCounter = 0
		#Normal Message
		else:
			nextCommand = chatterParser.getNextCommand()
			if(nextCommand == None):
				timeoutCounter += 1
		
		
		
		#Do something with it
		if(nextCommand != None):

			if(re.match(r'^up', nextCommand)):
				myMessage = messageGen.getMoveMessage('up')
				myTwitchChatter.sendMessage(myMessage)
				print myMessage
				move((1,0), 10)

			if(re.match(r'^left', nextCommand)):
				myMessage = messageGen.getMoveMessage('left')
				myTwitchChatter.sendMessage(myMessage)
				print myMessage
				move((0,1), 10)
				
			if(re.match(r'^right', nextCommand)):
				myMessage = messageGen.getMoveMessage('right')
				myTwitchChatter.sendMessage(myMessage)
				print myMessage
				move((0,-1), 10)
				
			#Stop!
			if(re.match(r'^stop', nextCommand)):
				chatterParser.stop()
				myTwitchChatter = None
				break
				


		#signal.signal(signal.SIGINT, handler)
		time.sleep(0.1)
		
	print 'Done'

