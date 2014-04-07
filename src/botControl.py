#!/usr/bin/env python

import rospy
from geometry_msgs.msg import *
from sensor_msgs.msg import *

#import time
import re

from twitchChatter import twitchChatter

obstacle_near = False


def laserCallback(data):
    global obstacle_near

    obstacle_distance_threshold = 2.0

    print 'Got new laser scan at ', rospy.Time.now()
    min_range = data.range_max
    for i in range(len(data.ranges)):
        if data.ranges[i] < min_range:
            min_range = data.ranges[i]

    print 'Minimum range from scan is : ', min_range
    if min_range < obstacle_distance_threshold:
        obstacle_near = True
    else:
        obstacle_near = False


#General movement Function
def move(inDir, maxTicks):
	global twist
	global obstacle_near
	
	tick = 0
	
	twist = inDir
	
	while(tick < maxTicks):
		tick += 1
		#rospy.sleep(0.1)
		time.sleep(0.1)
		
		if(obstacle_near):
			avoidObstical()
			break
			
		twist.linear.x = inDir[0]
		twist.angular.z = inDir[1]
		
		pub.publish(twist)

#Moves to make if we run into an obstacle	
def avoidObstical():
	move((-1, 0), 10)
	move((0, 1), 10)

	

#Main Loop
if __name__ == '__main__':
    rospy.init_node('bouncer', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.Subscriber("base_scan", LaserScan, laserCallback) 
    
	twist = Twist()
	
	chatReader = twitchChatter()
	while(True):
		newMessage = chatReader.getMessage()
		
		if(re.match(r'^up', newMessage[1])):
			move((1,0), 10)
			
		if(re.match(r'^left', newMessage[1])):
			move((0,1), 10)
			
		if(re.match(r'^right', newMessage[1])):
			move((0,-1), 10)

			
	print 'Done'

