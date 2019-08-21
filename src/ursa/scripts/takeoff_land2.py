#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import mavros_msgs.srv
import mavros_msgs.msg
import ursa.srv
import tf2_ros
import tf2_geometry_msgs
import threading
import nav_msgs.msg

setpoint = geometry_msgs.msg.TransformStamped()
takeOff=False
tf_buffer = tf2_ros.Buffer(rospy.Duration(10.0)) #tf buffer length

def set_position_thread():
    rate = rospy.Rate(20)
    br = tf2_ros.TransformBroadcaster()
    while True:
        setpoint.header.stamp = rospy.Time.now()
        br.sendTransform(setpoint)
        rate.sleep()

def setpoint_land():
    setpoint.transform.translation.z = -0.1
    rospy.sleep(4)
    if takeOff == False:
        arm(False)

def handle_takeoff_land(data):
    global setpoint
    global takeOff
    if data.takeoff and data.height <= 0.99:
        setpoint.transform.translation.z=data.height
        set_mode(0, "OFFBOARD")
        arm(True)
        takeOff = True
        return ursa.srv.TakeoffLandResponse(1)
    elif data.height>2.5:
        return ursa.srv.TakeoffLandResponse(-1)
    elif not data.takeoff:
        t = threading.Thread(target=setpoint_land)
        t.daemon = True
        takeOff = False
        t.start()
        return ursa.srv.TakeoffLandResponse(1)



if __name__ == '__main__':
    rospy.init_node('ursa_controller', anonymous=True)
    rate = rospy.Rate(20)

    # Init setpoint xform
    setpoint.header.frame_id = "map"
    setpoint.child_frame_id = "attitude"
    setpoint.transform.rotation.w = 1


    # setup services as client
    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    # setup services as server
    rospy.Service('ursa_takeoff_land', ursa.srv.TakeoffLand, handle_takeoff_land)

    # start tf publisher thread
    t = threading.Thread(target=set_position_thread)
    t.start()

    rospy.spin()
