#!/usr/bin/env python
import rospy
import std_msgs.msg 
import sensor_msgs.msg

hot_ang = []
tmp_scan = sensor_msgs.msg.LaserScan()
pub = rospy.Publisher('/thermal_scan', std_msgs.msg.String, queue_size=10)

def imageCB(data):
    #find angles corresponding to hot obj and modify the tmp_scan, then publish
    
    pub.publish(tmp_scan)

def ScanCB(data):
    #Store laser scan data
    tmp_scan = data
    
def find_hot():
    
    rospy.Subscriber("/teraranger_evo_thermal/raw_temp_array", std_msgs.msg.Float64MultiArray, imageCB)
    rospy.Subscriber("/laser/scan", sensor_msgs.msg.LaserScan, ScanCB)


if __name__ == '__main__':
    rospy.init_node('thermal_scan', anonymous=True)
    find_hot()

    rospy.spin()