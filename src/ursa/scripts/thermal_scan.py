#!/usr/bin/env python

import rospy
import std_msgs.msg 
import sensor_msgs.msg
import numpy as np

hot_scan = sensor_msgs.msg.LaserScan()
hot_scan.angle_min = -27925
hot_scan.angle_max = 0.27925
hot_scan.angle_increment = 0.01745
hot_scan.range_min = 0.03
hot_scan.range_max = 5.6
hot_scan.header.frame_id = 'thermal_frame'

pub = rospy.Publisher('/thermal_scan', sensor_msgs.msg.LaserScan, queue_size=10)

def imageCB(data):
    #find angles corresponding to hot obj then publish a rough estimate laserscan
    global hot_scan
    tmp = np.zeros(32)
    
    for i in range(0,32): #col
        for j in range(10,20): #row
            tmp[i] = tmp[i] + data.data[32*j+i]

    tmp_mask = (tmp>200)*1
    #print(tmp)
    #print(tmp_mask)
    ranges = np.multiply(np.divide(2000,tmp) + 1, tmp_mask) #Publish points between 1 and 2m
    hot_scan.ranges = ranges    
    hot_scan.header.stamp = rospy.Time.now()
    pub.publish(hot_scan)


if __name__ == '__main__':
    rospy.init_node('thermal_scan', anonymous=True)
    rospy.Subscriber("/teraranger_evo_thermal/raw_temp_array", std_msgs.msg.Float64MultiArray, imageCB)

    rospy.spin()
