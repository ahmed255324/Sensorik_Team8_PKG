#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import sys

def geschwindigkeit_regler():
    joy_pub = Joy()
    joy_pub.axes[0] = 0.1
    #joy_pub.axes[3] = 0.6
    rospy.init_node('P_geschwindigkeit_regler', anonymous=True)
    pub = rospy.Publisher('/joy', Joy, queue_size=1)
    rate = rospy.Rate(10) # 10 hz
    #keep publishing until a Ctrl-C is pressed
    while not rospy.is_shutdown():
        pub.publish(joy_pub)
        rate.sleep()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        #print("Die Nutzung von geschwindigkeit_regler.py mit defoalt arg1 arg2")
        geschwindigkeit_regler()
    else:
        geschwindigkeit_regler()
