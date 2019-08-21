#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import mavros_msgs.srv
import mavros_msgs.msg
import tf2_ros
from pynput import keyboard
from geometry_msgs.msg import Twist

# setup node
rospy.init_node('ursa_controller', anonymous=True)
rate = rospy.Rate(20)
set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
x = 0; z = 0
pub = rospy.Publisher('tmp_cmd_vel', Twist, queue_size=10)
tmp_cmd_vel = Twist()
def set_position(x, z):

    tmp_cmd_vel.linear.x = x
    tmp_cmd_vel.angular.z = z
    pub.publish(tmp_cmd_vel)


def on_press(key):
    global x, y, z
    MOVEMENT_SENSITIVITY = 0.1

    try: k = key.char
    except: k = key.name

    # determine actions on key press
    if k == 'left':
        print 'left command received...'
        z -= MOVEMENT_SENSITIVITY
        set_position(x,z)
    elif k == 'right':
        print 'right command received...'
        z += MOVEMENT_SENSITIVITY
        set_position(x,z)
        print(x)
    elif k == 'down':
        print 'down command received...'
        x -= MOVEMENT_SENSITIVITY
        set_position(x,z)
        print(x)
    elif k == 'up':
        print 'up command received...'
        x += MOVEMENT_SENSITIVITY
        set_position(x,z)
    elif k == 't':
        print 'takeoff command received...'
        z = 0.3
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
    #rate.sleep()

if __name__ == '__main__':
    lis = keyboard.Listener(on_press=on_press)
    lis.start()

    rospy.spin()




