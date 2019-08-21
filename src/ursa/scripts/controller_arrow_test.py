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
import tf_conversions
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

def waypointCB(data):
    global setpoint
    transform = tf_buffer.lookup_transform("map",
                                       "map", #source frame
                                       rospy.Time(0), #get the tf at first available time
                                       rospy.Duration(1.0)) #wait for 1 second

    # If goal is inside robot foot print then setpoint as goal opposed to local plan
    # Commented out in response to issue #2.  Set local planner orientation in trajectory generator when inside robot radius.
    # if (((current_pose.pose.position.x - robot_radius) < global_plan_endpoint.pose.position.x) and
    #     (global_plan_endpoint.pose.position.x < (current_pose.pose.position.x + robot_radius)) and
    #     ((current_pose.pose.position.y - robot_radius) < global_plan_endpoint.pose.position.y) and
    #     (global_plan_endpoint.pose.position.y < (current_pose.pose.position.y + robot_radius))):
    #     mapPose = global_plan_endpoint
    # else:
    #     mapPose = tf2_geometry_msgs.do_transform_pose(data.poses[-1], transform)
    #mapPose = tf2_geometry_msgs.do_transform_pose(data, transform)
    setpoint.transform.translation.x = data.pose.position.x
    setpoint.transform.translation.y = data.pose.position.y
    setpoint.transform.rotation.x = data.pose.orientation.x
    setpoint.transform.rotation.y = data.pose.orientation.y
    setpoint.transform.rotation.z = data.pose.orientation.z
    setpoint.transform.rotation.w = data.pose.orientation.w

if __name__ == '__main__':
    rospy.init_node('ursa_controller', anonymous=True)
    rate = rospy.Rate(20)

    # Init setpoint xform
    setpoint.header.frame_id = "map"
    setpoint.child_frame_id = "attitude"
    setpoint.transform.rotation.w = 1

    # listen for nav stuff
    local_plan_sub = rospy.Subscriber('/ursa_target', geometry_msgs.msg.PoseStamped, waypointCB, queue_size=10)

    # setup services as client
    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

    # setup services as server
    rospy.Service('ursa_takeoff_land', ursa.srv.TakeoffLand, handle_takeoff_land)

    # start tf publisher thread
    t = threading.Thread(target=set_position_thread)
    t.start()

    rospy.spin()
