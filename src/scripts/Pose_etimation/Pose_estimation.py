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

video_capture1 = cv2.VideoCapture(4, cv2.CAP_V4L2)
video_capture1.release()
video_capture1 = cv2.VideoCapture(4, cv2.CAP_V4L2)
video_capture2 = cv2.VideoCapture(0, cv2.CAP_V4L2)
video_capture2.release()
video_capture2 = cv2.VideoCapture(0, cv2.CAP_V4L2)
video_capture3 = cv2.VideoCapture(2, cv2.CAP_V4L2)
video_capture3.release()
video_capture3 = cv2.VideoCapture(2, cv2.CAP_V4L2)


a = 190

cameraMatrix_1 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/cameraMatrix_1.csv", delimiter=',')
cameraMatrix_2 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/cameraMatrix_2.csv", delimiter=',')
cameraMatrix_3 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/cameraMatrix_3.csv", delimiter=',')

dist_1 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/dist_1.csv', delimiter=',')
dist_2 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/dist_2.csv', delimiter=',')
dist_3 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/dist_3.csv', delimiter=',')

objectPoints = np.random.random((4,3,1))
imagePoints = np.random.random((4,2,1))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objectPoints[0] = [[-a/2], [a/2], [0]]
objectPoints[1] = [[-a/2], [-a/2], [0]]
objectPoints[2] = [[a/2], [-a/2], [0]]
objectPoints[3] = [[a/2], [a/2], [0]]


tf_1 = np.zeros((4,4))	
tf_2 = np.zeros((4,4))
tf_3 = np.zeros((4,4))
tf= np.zeros((4,4))

while(not rospy.is_shutdown()):

	ret1, frame1 = video_capture1.read()
	if ret1:
		code1 = decode(frame1)
		for qrcode1 in code1:
			print('1')

	ret2, frame2 = video_capture2.read()
	if ret2:
		code2 = decode(frame2)
		for qrcode2 in code2:
			print('2')
	
	ret3, frame3 = video_capture3.read()
	if ret3:
		code3 = decode(frame3)
		for qrcode3 in code3:
			print('3')

	#frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	#frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
	#frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
	
video_capture1.release()
video_capture2.release()
video_capture3.release()