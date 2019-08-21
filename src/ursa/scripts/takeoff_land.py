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

setpoint = geometry_msgs.msg.PoseStamped()
takeOff=False
tf_buffer = tf2_ros.Buffer(rospy.Duration(10.0)) #tf buffer length
pub = rospy.Publisher('mavros/setpoint_attitude/target_attitude', geometry_msgs.msg.PoseStamped, queue_size=10)

def setArm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e
def setLandMode():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        landService(altitude=0, latitude=0, longitude=0, min_pitch=0, yaw=0)
    except rospy.ServiceException, e:
        print "Service land call failed: %s"%e

def setTakeoffMode():
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
        takeoffService(altitude=2, latitude=0, longitude=0, min_pitch=0, yaw=0)
    except rospy.ServiceException, e:
        print "Service takeoff call failed: %s"%e
def setOffboard():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        offboardService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        offboardService("OFFBOARD", 0)
    except rospy.ServiceException, e:
        print "Service offboard mode call failed: %s"%e

def setpoint_buffer():
    for i in range(10):
        print i
        pub.publish(setpoint)
        rate.sleep()

def set_position_thread():
    rate = rospy.Rate(20)

    pub.publish(setpoint)


def setpoint_land():
    setpoint.pose.position.z = -0.1
    rospy.sleep(4)
    if takeOff == False:
        arm(False)

def handle_takeoff_land(data):
    global setpoint
    global takeOff
    #setpoint_buffer()
    if data.takeoff and data.height <= 0.99:
        setpoint.pose.position.z=data.height
        #setpoint.pose.orientation.w=1
        setOffboard()
        setArm()
        #setTakeoffMode()
        takeOff = True
        return ursa.srv.TakeoffLandResponse(1)
    elif data.height>2.5:
        return ursa.srv.TakeoffLandResponse(-1)
    elif not data.takeoff:
        #t = threading.Thread(target=setpoint_land)
        #t.daemon = True
        setLandMode()
        takeOff = False
        t.start()
        return ursa.srv.TakeoffLandResponse(1)


if __name__ == '__main__':
    rospy.init_node('takeoff_land', anonymous=True)
    rate = rospy.Rate(20)

    rospy.Service('ursa_takeoff_land', ursa.srv.TakeoffLand, handle_takeoff_land)

    # start tf publisher thread
    #t = threading.Thread(target=set_position_thread)
    #t.start()

    rospy.spin()
