#!/usr/bin/env python

from math import pi
import cv2 
from pyzbar.pyzbar import decode
import numpy as np
from sympy import true
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

video_capture1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
fps = int(video_capture1.get(5))
print("fps:", fps)

video_capture2 = cv2.VideoCapture(2, cv2.CAP_V4L2)
fps = int(video_capture2.get(5))
print("fps:", fps)

a = 190
cameraMatrix_1 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/cameraMatrix_1.csv", delimiter=',')
cameraMatrix_2 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/cameraMatrix_2.csv", delimiter=',')

dist_1 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/dist_1.csv', delimiter=',')
dist_2 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/dist_2.csv', delimiter=',')

objectPoints = np.random.random((4,3,1))
imagePoints = np.random.random((2,2,1))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objectPoints[0] = [[-a/2], [a/2], [0]]
objectPoints[1] = [[-a/2], [-a/2], [0]]
objectPoints[2] = [[a/2], [-a/2], [0]]
objectPoints[3] = [[a/2], [a/2], [0]]


tf_1 = np.zeros((4,4))	
tf_2 = np.zeros((4,4))
tf= np.zeros((4,4))

tow = 0

while(not rospy.is_shutdown()):
	ret1, frame1 = video_capture1.read()
	code1 = decode(frame1)
	for qrcode1 in code1:
		barcodeData_1 = qrcode1.data.decode("utf-8")
		points = np.array(code1[0].polygon, np.int32)
		imagePoints[tow] = [[points[0][0]], [points[0][1]]]
		tow = tow + 1
	if(tow == 2):
		x = imagePoints[0] - imagePoints[1]
		print(x)
	
	tow = 0
	ret2, frame2 = video_capture2.read()
	code2 = decode(frame2)
	for qrcode2 in code2:
		barcodeData_2 = qrcode2.data.decode("utf-8")
		points = np.array(code2[0].polygon, np.int32)
		imagePoints[tow] = [[points[0][0]], [points[0][1]]]
		
	if(code1):
		if(code2):
			tf = (tf_1 + tf_2)/2
		else:
			tf = tf_1
		
	elif(code2):
		if(code1):
			tf = (tf_1 + tf_2)/2
		else:
			tf = tf_2

	if(code1 or code2):	
		pose_o.pose.position.x = tf[0][3] 
		pose_o.pose.position.y = tf[1][3]
		pose_o.pose.position.z = 0
		pose_a.X = tf[0][3]
		pose_a.Y = tf[1][3]
		M1 = tf[0:3, 0:3]

		eulerW = funktionen.eulerAnglesToRotationMatrix(M1)			
		pose_a.Z = eulerW[2]*(180/pi)
		# Quaternion
		if((float(1)+M1[0,0]+M1[1,1]+M1[2,2]) > 0 ):
			r = np.math.sqrt(float(1)+M1[0,0]+M1[1,1]+M1[2,2])*0.5
			i = (M1[2,1]-M1[1,2])/(4*r)
			j = (M1[0,2]-M1[2,0])/(4*r)
			k = (M1[1,0]-M1[0,1])/(4*r)
			pose_o.pose.orientation.x = r
			pose_o.pose.orientation.y = i
			pose_o.pose.orientation.z = k
			pose_o.pose.orientation.w = j
			
		pub.publish(pose_o)
		puba.publish(pose_a)
		pubm.publish(empty_message)

video_capture1.release()
video_capture2.release()