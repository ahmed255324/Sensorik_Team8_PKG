#!/usr/bin/env python

import rospy
from Sensorik_Team8_PKG.msg import movecontrol

def geschwindigkeit_regler():
    steuerung = movecontrol()
    steuerung.geschwindigkeit = 0.4
    steuerung.lenkung = 
    rospy.init_node("P_geschwindigkeit_regler", anonymous=True)
    pub = rospy.Publisher("/movecontrol", movecontrol, queue_size=1)
    rate = rospy.Rate(100) # 10 hz
    #keep publishing until a Ctrl-C is pressed
    while not rospy.is_shutdown():
        pub.publish(steuerung)
        rate.sleep()
    steuerung.geschwindigkeit = 0.0
    steuerung.lenkung = 0.0
    pub.publish(steuerung)

if __name__ == '__main__':
    geschwindigkeit_regler()
        
