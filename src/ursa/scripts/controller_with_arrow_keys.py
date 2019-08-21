#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import mavros_msgs.srv
import mavros_msgs.msg
from sensor_msgs.msg import LaserScan
import tf2_ros
from pynput import keyboard
import tf_conversions
# setup node
rospy.init_node('ursa_controller', anonymous=True)
rate = rospy.Rate(20)
set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
x = 0; theta = 0.1; z = 1
MAX_DIST = 1
laser = LaserScan()
regions = {}
state = mavros_msgs.msg.State()
def set_position(x, theta, z):
    br = tf2_ros.TransformBroadcaster()
    setpoint = geometry_msgs.msg.TransformStamped()

    setpoint.header.stamp = rospy.Time.now()
    setpoint.header.frame_id = "map"
    setpoint.child_frame_id = "setpoint"
    
    q = tf_conversions.transformations.quaternion_from_euler(0, 0, theta)
    print 'hahaaha'
    setpoint.transform.translation.x = x
    setpoint.transform.translation.z = z
    setpoint.transform.rotation.x = q[0]
    setpoint.transform.rotation.y = q[1]
    setpoint.transform.rotation.z = q[2]
    setpoint.transform.rotation.w = q[3]

    br.sendTransform(setpoint)

def setpoint_buffer(x, y, z):
    for i in range(10):
        print i,
        set_position(x, y, z)
        rate.sleep()

def on_press(key):
    global x, theta, z, laser
    MOVEMENT_SENSITIVITY = 0.1

    try: k = key.char
    except: k = key.name

    # determine actions on key press
    if k == 'up' and not warning():
        print 'forward command received...'
        x += MOVEMENT_SENSITIVITY
        set_position(x, theta, z)

    elif k == 'down':
        print 'reverse command received...'
        x -= MOVEMENT_SENSITIVITY
        set_position(x, theta, z)
    elif k == 'right':
        print 'turn right command received...'
        theta -= MOVEMENT_SENSITIVITY
        set_position(x, theta, z)
    elif k == 'left':
        print 'turn left command received...'
        theta += MOVEMENT_SENSITIVITY
        set_position(x, theta, z)
    elif k == 'w':
        print 'up command received...'
        z += MOVEMENT_SENSITIVITY
        set_position(x, theta, z)
    elif k == 's':
        print 'down command received...'
        z -= MOVEMENT_SENSITIVITY
        set_position(x, theta, z)

    elif k == 't':
        print 'takeoff command received...'
        #while(state.mode != "OFFBOARD"):
        for i in range(10):
            set_position(x, theta, z)
            set_mode(0, "OFFBOARD")
            arm(True) 
    elif k == 'l':
        print 'land command received...'
        set_mode(0, "AUTO.LAND")
        previous_input = 'l'
    elif k == 'd':
        print 'disarm command received...'
        arm(False)

    print "key pressed"
    rate.sleep()

def laser_callback(laser):
    names = ['right', 'fright','fleft', 'left']
    num_of_regions = 4
    segment = len(laser.ranges)//num_of_regions
    for i in range(num_of_regions):
        regions[names[i]] = min(laser.ranges[((i)*segment):((i+1)*(segment)-1)])
        #print(regions)
def warning():
    global regions
    warning_flag = False
    if (regions['fleft'] < MAX_DIST or regions['fright'] < MAX_DIST):
        state_description = "Watch out!"
        warning_flag = True
    return warning_flag
def state_callback(msg):
    state = msg

if __name__ == '__main__':
    lis = keyboard.Listener(on_press=on_press)
    lis.start()

    # setup services as client
    set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
    rospy.Subscriber('scan_filtered_nans', LaserScan, laser_callback)
    #rospy.Subscriber('/mavros/state', mavros_msgs.msg.State, state_callback)
    rospy.spin()




