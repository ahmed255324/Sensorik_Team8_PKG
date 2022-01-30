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
import pygame
import pygame.camera

rospy.init_node('Pose_estimation', anonymous=True)
pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
puba = rospy.Publisher('/Auswertung', auswertungsmessage, queue_size=10)
pubm = rospy.Publisher('/Messung', Empty, queue_size=10)
pose_o = ModelState()
pose_a = auswertungsmessage()
empty_message = Empty()
pose_o.model_name = "unit_box"

# initializing  the camera
pygame.camera.init()
  
# make the list of all available cameras
camlist = pygame.camera.list_cameras()

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

cam_2 = 1
cam_3 = 10
win = 0

# initializing the cam variable with default camera
cam_2 = pygame.camera.Camera(camlist[0], (640, 480))
cam_3 = pygame.camera.Camera(camlist[2], (640, 480))

# opening the camera
cam_2.start()
cam_3.start()

while(not rospy.is_shutdown()):
	image = cam_2.get_image()
	view = pygame.surfarray.array3d(image)
	view = view.transpose([1, 0, 2])
	#  convert from rgb to bgr
	frame2 = cv2.cvtColor(view, cv2.COLOR_RGB2BGR) 
	code2 = decode(frame2)
	for qrcode2 in code2:
		barcodeData_2 = qrcode2.data.decode("utf-8")
		points = np.array(code2[0].polygon, np.float32)
		if((4,2) == np.shape(points)):
			imagePoints = np.reshape(points, (4,2,1))
			flag_2, rvecs_2, tvecs_2 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_2, dist_2, flags=cv2.SOLVEPNP_P3P)
			tf_2 = funktionen.TF(rvecs=rvecs_2, tvecs=tvecs_2)
			tf_2 = np.dot(tabelle.qrcode_tf[int(barcodeData_2)-1], tf_2)
			tf_2 = np.dot(tf_2, [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
			win = win + int(barcodeData_2)

	image = cam_3.get_image()
	view = pygame.surfarray.array3d(image)
	view = view.transpose([1, 0, 2])
	#  convert from rgb to bgr
	frame3 = cv2.cvtColor(view, cv2.COLOR_RGB2BGR) 
	code3 = decode(frame3)
	for qrcode3 in code3:
		barcodeData_3 = qrcode3.data.decode("utf-8")
		points = np.array(code3[0].polygon, np.float32)
		if((4,2) == np.shape(points)):
			imagePoints = np.reshape(points, (4,2,1))
			_, rvecs_3, tvecs_3 = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix_3, dist_3, flags=cv2.SOLVEPNP_P3P)
			tf_3 = funktionen.TF(rvecs=rvecs_3, tvecs=tvecs_3)
			tf_3 = np.dot(tabelle.qrcode_tf[int(barcodeData_3)-1], tf_3)
			tf_3 = np.dot(tf_3, [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, -0.1], [0, 0, 0, 1]])
			win = win + int(barcodeData_3)
	
	if(code3 or code2):
		pose_o.pose.position.x = tf_3[0][3] 
		pose_o.pose.position.y = tf_2[1][3]
		print(tf_3[0][3], tf_2[1][3])
		pose_a.X = tf_3[0][3]
		pose_a.Y = tf_2[1][3]
		angle = funktionen.Angle(win)
		pose_a.Z = angle * (180/pi)
		# Quaternion
		pose_o.pose.orientation.x = 0
		pose_o.pose.orientation.y = 0
		pose_o.pose.orientation.z, pose_o.pose.orientation.w  = funktionen.Angle(angle)	
		pub.publish(pose_o)
		puba.publish(pose_a)
		pubm.publish(empty_message)
		win = 0