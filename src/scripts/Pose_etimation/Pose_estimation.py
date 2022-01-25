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

video_capture1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not video_capture1.isOpened():
    print("Cannot open camera 1")
    exit()
video_capture2 = cv2.VideoCapture(2, cv2.CAP_V4L2)
if not video_capture2.isOpened():
    print("Cannot open camera 2")
    exit()
video_capture3 = cv2.VideoCapture(4, cv2.CAP_V4L2)
if not video_capture3.isOpened():
    print("Cannot open camera 3")
    exit()

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
			barcodeData_1 = qrcode1.data.decode("utf-8")
			points = np.array(code1[0].polygon, np.int32)
			imagePoints[0] = [[points[0][0]], [points[0][1]]]
			imagePoints[1] = [[points[1][0]], [points[1][1]]]
			imagePoints[2] = [[points[2][0]], [points[2][1]]]
			imagePoints[3] = [[points[3][0]], [points[3][1]]]
			_, rvecs_1, tvecs_1 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_1, dist_1, flags=cv2.SOLVEPNP_P3P)
			tf_1 = funktionen.TF(rvecs=rvecs_1, tvecs=tvecs_1)
			tf_1 = np.dot(tabelle.qrcode_tf[int(barcodeData_1)-1], tf_1)
			tf_1 = np.dot(tf_1, [[-1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
			print('1')

	ret2, frame2 = video_capture2.read()
	if ret2:
		code2 = decode(frame2)
		for qrcode2 in code2:
			barcodeData_2 = qrcode2.data.decode("utf-8")
			points = np.array(code2[0].polygon, np.int32)
			imagePoints[0] = [[points[0][0]], [points[0][1]]]
			imagePoints[1] = [[points[1][0]], [points[1][1]]]
			imagePoints[2] = [[points[2][0]], [points[2][1]]]
			imagePoints[3] = [[points[3][0]], [points[3][1]]]
			_, rvecs_2, tvecs_2 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_2, dist_2, flags=cv2.SOLVEPNP_P3P)
			tf_2 = funktionen.TF(rvecs=rvecs_2, tvecs=tvecs_2)
			tf_2 = np.dot(tabelle.qrcode_tf[int(barcodeData_2)-1], tf_2)
			tf_2 = np.dot(tf_2, [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
			print('2')
	ret3, frame3 = video_capture3.read()

	if ret3:
		code3 = decode(frame3)
		for qrcode3 in code3:
			barcodeData_3 = qrcode3.data.decode("utf-8")
			points = np.array(code3[0].polygon, np.int32)
			imagePoints[0] = [[points[0][0]], [points[0][1]]]
			imagePoints[1] = [[points[1][0]], [points[1][1]]]
			imagePoints[2] = [[points[2][0]], [points[2][1]]]
			imagePoints[3] = [[points[3][0]], [points[3][1]]]
			_, rvecs_3, tvecs_3 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_3, dist_3, flags=cv2.SOLVEPNP_P3P)
			tf_3 = funktionen.TF(rvecs=rvecs_3, tvecs=tvecs_3)
			tf_3 = np.dot(tabelle.qrcode_tf[int(barcodeData_3)-1], tf_3)
			tf_3 = np.dot(tf_3, [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, -0.1], [0, 0, 0, 1]])
			print('3')

	#frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	#frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
	#frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
	
video_capture1.release()
video_capture2.release()
video_capture3.release()