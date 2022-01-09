#!/usr/bin/env python
# license removed for brevity
import rospy
from Sensorik_Team8_PKG.msg import joy_axes
from sensor_msgs.msg import Joy

joypub = joy_axes()
def callback(data):
    global joypub
    joypub.motor = int(100 * data.axes[1])
    joypub.linker = int(100 * data.axes[3])
    pub.publish(joypub)

rospy.init_node('python_umwandler', anonymous=True)
pub = rospy.Publisher('/arduino_steuerung', joy_axes, queue_size=30)
rospy.Subscriber("/joy", Joy, callback)

rospy.spin()


#/ 13107.0
