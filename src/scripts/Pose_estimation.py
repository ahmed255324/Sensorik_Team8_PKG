#!/usr/bin/env python

import cv2
from pyzbar.pyzbar import decode
import numpy as np
import rospy
from gazebo_msgs.msg import ModelState
import tabelle

rospy.init_node('Pose_estimation', anonymous=True)
pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
pose_o = ModelState()
pose_o.model_name = "unit_box"

def TF(rvecs, tvecs):
	tf = np.zeros((4,4), dtype= float)
	rotation_matrix = np.transpose(cv2.Rodrigues(rvecs)[0])
	tf[0:3, 0:3] = rotation_matrix
	tf[3][3] = 1
	tf[0:3, 3:4] = np.dot(-rotation_matrix, tvecs)/1000
	return tf

video_capture1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
video_capture2 = cv2.VideoCapture(2, cv2.CAP_V4L2)
#video_capture3 = cv2.VideoCapture(4)

a = 190
b = 190

cameraMatrix_1 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/cameraMatrix_1.csv", delimiter=',')
cameraMatrix_2 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/cameraMatrix_2.csv", delimiter=',')
#cameraMatrix_3 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/cameraMatrix_3.csv", delimiter=',')

dist_1 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_1/dist_1.csv', delimiter=',')
dist_2 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/dist_2.csv', delimiter=',')
#dist_3 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/dist_3.csv', delimiter=',')

objectPoints = np.random.random((4,3,1))
imagePoints = np.random.random((4,2,1))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objectPoints[0] = [[0], [0], [0]]
objectPoints[1] = [[0], [a], [0]]
objectPoints[2] = [[-b], [a], [0]]
objectPoints[3] = [[-b], [0], [0]]

tf_1 = np.zeros((4,4))	
tf_2 = np.zeros((4,4))
tf_3 = np.zeros((4,4))

while(not rospy.is_shutdown()): #not rospy.is_shutdown():

	ret1, frame1 = video_capture1.read()
	ret2, frame2 = video_capture2.read()
	#ret3, frame3 = video_capture3.read()

	code1 = decode(frame1)
	code2 = decode(frame2)
	#code3 = decode(frame3)

	for qrcode1 in code1:
		barcodeData_1 = qrcode1.data.decode("utf-8")
		print(barcodeData_1)
		points = np.array(code1[0].polygon, np.int32)
		imagePoints[0] = [[points[0][0]], [points[0][1]]]
		imagePoints[1] = [[points[1][0]], [points[1][1]]]
		imagePoints[2] = [[points[2][0]], [points[2][1]]]
		imagePoints[3] = [[points[3][0]], [points[3][1]]]
		_, rvecs_1, tvecs_1 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_1, dist_1, flags=cv2.SOLVEPNP_P3P)
		tf_1 = TF(rvecs=rvecs_1, tvecs=tvecs_1)
		tf = tf_1 * tabelle.qrcode_tf[barcodeData_1-1]
		print(tf[0:3, 3:4])

	for qrcode2 in code2:
		barcodeData_2 = qrcode2.data.decode("utf-8")
		points = np.array(code2[0].polygon, np.int32)
		imagePoints[0] = [[points[0][0]], [points[0][1]]]
		imagePoints[1] = [[points[1][0]], [points[1][1]]]
		imagePoints[2] = [[points[2][0]], [points[2][1]]]
		imagePoints[3] = [[points[3][0]], [points[3][1]]]
		_, rvecs_2, tvecs_2 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_2, dist_2, flags=cv2.SOLVEPNP_P3P)
		tf_2 = TF(rvecs=rvecs_2, tvecs=tvecs_2)
		tf = tf_2 * tabelle.qrcode_tf[barcodeData_1-1]

	#pose_o.pose.position.x = tvecs[0]
	#pose_o.pose.position.y = tvecs[1]
	#pose_o.pose.position.z = tvecs[2]
	#pose_o.pose.orientation.x = 0
	#pose_o.pose.orientation.y = 0
	#pose_o.pose.orientation.z = 0
	#pose_o.pose.orientation.w = 0
	#pub.publish(pose_o)

video_capture1.release()
video_capture2.release()
#video_capture3.release()