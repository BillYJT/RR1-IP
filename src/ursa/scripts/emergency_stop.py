#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
"""
RR1-IP Guoxin
The main idea is to divide the scanned area into five regions. It is not necessary though if we care about all the directions.
In this case we can use 'data.range_min' http://docs.ros.org/melodic/api/sensor_msgs/html/msg/LaserScan.html  .
"""
pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=1)
MAX_DIST = 1
class Server: 
	def __init__(self):
		self.laser = None
		self.Remote_Vel = None
		self.regions = None
	def laser_callback(self,msg):
		self.laser = msg
		self.divide_region()
	def Remote_Vel_callback(self,msg):
		self.Remote_Vel = msg
		self.calm_down()

	def divide_region(self):		
		names = ['right', 'fright', 'front', 'fleft', 'left']
		num_of_regions = 5
		segment = len(self.laser.ranges)//num_of_regions
		self.regions = {}
		for i in range(num_of_regions):
			self.regions[names[i]] = min(self.laser.ranges[((i)*segment):((i+1)*(segment)-1)])
	def calm_down(self):
		msg = self.Remote_Vel
		state_description = ''
		if self.regions is not None and self.Remote_Vel is not None:
			if (self.regions['front'] < MAX_DIST or self.regions['fleft'] < MAX_DIST or self.regions['fright'] < MAX_DIST) and msg.linear.x > 0:
				state_description = "Watch out!"
				msg.linear.x = 0
				msg.angular.z = 0
				#msg = 0
				
		
			state_description = "Safty scan on duty!"
			pub.publish(msg)
			rospy.loginfo(state_description)
			



if __name__ == '__main__':
	rospy.init_node('emergency_stop', anonymous=True)
	server = Server()
	rospy.Subscriber('scan_filtered_nans', LaserScan, laser_callback)
	rospy.Subscriber('tmp_cmd_vel', Twist, server.Remote_Vel_callback)
	rospy.spin()
