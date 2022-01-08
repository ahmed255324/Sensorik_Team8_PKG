from std_msgs.msg import Empty
from Sensorik_Team8_PKG.msg import geschwindigkeitUndMessrate
import rospy
import time
from datetime import datetime

mesrate_o = geschwindigkeitUndMessrate()
time_0 = 0
time_1 = 0
def callback(data):
    global mesrate_o, time_0, time_1
    time_1 = datetime.now()
    difference = time_1 - time_0
    mesrate_o = difference.total_seconds()
    pub.publish(mesrate_o)

rospy.init_node('messrate_node', anonymous=True)
pub = rospy.Publisher('/gundm', geschwindigkeitUndMessrate, queue_size=1)
rospy.Subscriber("/Messung", Empty, callback)

rospy.spin()