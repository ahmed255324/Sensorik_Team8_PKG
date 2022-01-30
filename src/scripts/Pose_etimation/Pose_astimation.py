#!/usr/bin/env python

from math import pi
import cv2 
from pyzbar.pyzbar import decode
import numpy as np
import rospy
from gazebo_msgs.msg import ModelState
from Sensorik_Team8_PKG.msg import auswertungsmessage
from std_msgs.msg import Empty
import tabelle
import funktionen

rospy.init_node('Pose_estimation', anonymous=True)
pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
puba = rospy.Publisher('/Auswertung', auswertungsmessage, queue_size=10)
pubm = rospy.Publisher('/Messung', Empty, queue_size=10)
pose_o = ModelState()
pose_a = auswertungsmessage()
empty_message = Empty()
pose_o.model_name = "unit_box"

video_capture2 = cv2.VideoCapture(0, cv2.CAP_V4L2)
fps = int(video_capture2.get(5))
print("fps:", fps)

video_capture3 = cv2.VideoCapture(2, cv2.CAP_V4L2)
fps = int(video_capture3.get(5))
print("fps:", fps)

a = 190

cameraMatrix_2 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/cameraMatrix_2.csv", delimiter=',')
cameraMatrix_3 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/cameraMatrix_3.csv", delimiter=',')

dist_2 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/dist_2.csv', delimiter=',')
dist_3 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/dist_3.csv', delimiter=',')

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objectPoints = np.array([[-a/2, a/2, 0], [-a/2, -a/2, 0], [a/2, -a/2, 0], [a/2, a/2, 0]], dtype=np.float32)
objectPoints = np.reshape(objectPoints, (4,3,1))
	
tf_2 = np.zeros((4,4))
tf_3 = np.zeros((4,4))

x = 0.0
y = 0.0

cam_2 = 1
cam_3 = 10
win = 0

while(not rospy.is_shutdown()):
	ret2, frame2 = video_capture2.read()
	code2 = decode(frame2)
	for qrcode2 in code2:
		barcodeData_2 = int(qrcode2.data.decode("utf-8"))
		points = np.array(code2[0].polygon, np.float32)
		if((4,2) == np.shape(points)):
			imagePoints = np.reshape(points, (4,2,1))
			_, _, tvecs_2 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_2, dist_2, flags=cv2.SOLVEPNP_P3P)
			if tvecs_2 is not None:
				tf_2[2] = tf_2[2] + 0.1
				tf_2 = np.dot(tabelle.qrcode_tf[barcodeData_2-1], funktionen.TF(tvecs_2))
				if(barcodeData_2 >= 1 and barcodeData_2 < 20):
					y = tf_2[1][3]
					print('y ',y)
				else:
					x = tf_2[0][3]
		win = win + barcodeData_2 * cam_2


	ret3, frame3 = video_capture3.read()
	code3 = decode(frame3)
	for qrcode3 in code3:
		barcodeData_3 = int(qrcode3.data.decode("utf-8"))
		points = np.array(code3[0].polygon, np.float32)
		if((4,2) == np.shape(points)):
			#print(barcodeData_3)
			imagePoints = np.reshape(points, (4,2,1))
			_, _, tvecs_3 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_3, dist_3, flags=cv2.SOLVEPNP_P3P)
			if tvecs_3 is not None:
				tf_3[2] = tf_3[2] + 0.1
				tf_3 = np.dot(tabelle.qrcode_tf[barcodeData_3-1], funktionen.TF(tvecs_3))
				if(barcodeData_3 >= 1 and barcodeData_3< 20):
					x = tf_3[0][3]
					print('x ', x)
				else:
					y = tf_3[1][3]
		win = win + barcodeData_3 * cam_3

	if(code3 or code2):
		pose_o.pose.position.x = x
		pose_o.pose.position.y = y
		pose_o.pose.position.z = 0.0
		#print(x, y)
		#print(tf_3[1][3], tf_2[1][3])
		pose_a.X = x
		pose_a.Y = y
		pose_o.pose.orientation.x = 0.0
		pose_o.pose.orientation.y = 0.0
		pose_o.pose.orientation.z = 0.0
		pose_o.pose.orientation.w = 0.0
			
		pub.publish(pose_o)
		puba.publish(pose_a)
		pubm.publish(empty_message)
	win = 0
video_capture3.release()
video_capture2.release()