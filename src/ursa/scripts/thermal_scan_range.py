#!/usr/bin/env python

import rospy
import std_msgs.msg 
import sensor_msgs.msg
import numpy as np
import math


hot_scan = sensor_msgs.msg.LaserScan()
hot_scan.angle_min = -2.35619449615
hot_scan.angle_max = 2.09234976768
hot_scan.angle_increment = 0.00613592332229
hot_scan.range_min = 0.03
hot_scan.range_max = 5.6
hot_scan.header.frame_id = 'thermal_frame'

pub = rospy.Publisher('/thermal_scan', sensor_msgs.msg.LaserScan, queue_size=10)
tmp_laserscan = np.zeros(90)

def imageCB(data):
    #find angles corresponding to hot obj then publish a rough estimate laserscan
    global tmp_laserscan
    tmp = np.zeros(90)
    i=1
    while i<=90: #col
        for j in range(10,20): #row
            tmp[i] = tmp[i] + data.data[32*j+math.ceil(i*0.351)]
        tmp[i+1] = tmp[i]
        tmp[i+2] = tmp[i]
        i = i + 3
    tmp = tmp/10
    tmp_mask = (tmp>30)*1

    hot_scan.ranges = tmp_mask*tmp_laserscan    
    hot_scan.intensities = tmp_mask*tmp
    hot_scan.header.stamp = rospy.Time.now()
    pub.publish(hot_scan)

def scanCB(data):
    global tmp_laserscan
    tmp_laserscan = data.ranges[336:427] #from -16.5 to 16.5 deg


if __name__ == '__main__':
    rospy.init_node('thermal_scan', anonymous=True)
    rospy.Subscriber("/scan_filtered_nans", std_msgs.msg.LaserScan, scanCB)
    rospy.Subscriber("/teraranger_evo_thermal/raw_temp_array", std_msgs.msg.Float64MultiArray, imageCB)
    
    rospy.spin()