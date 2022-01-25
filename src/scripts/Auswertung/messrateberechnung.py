from std_msgs.msg import Empty
from Sensorik_Team8_PKG.msg import messrate
import rospy
import time
from datetime import datetime

mesrate_o = messrate()
time_0 = datetime.now()
time_1 = datetime
def callback(data):
    global mesrate_o, time_0, time_1
    time_1 = datetime.now()
    difference = time_1 - time_0
    mesrate_o.messrate = 1/difference.total_seconds()
    if(mesrate_o.messrate > 10):
        mesrate_o.messrate = 10
    pub.publish(mesrate_o)
    time_0 = time_1

rospy.init_node('messrate_node', anonymous=True)
pub = rospy.Publisher('/Pose_estimation_messrate', messrate, queue_size=1)
rospy.Subscriber("/Messung", Empty, callback)
rospy.spin()
