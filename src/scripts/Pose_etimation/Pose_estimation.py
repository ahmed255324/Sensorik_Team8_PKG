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
import threading

rospy.init_node('Pose_estimation', anonymous=True)
pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
puba = rospy.Publisher('/Auswertung', auswertungsmessage, queue_size=10)
pubm = rospy.Publisher('/Messung', Empty, queue_size=10)
pose_o = ModelState()
pose_a = auswertungsmessage()
empty_message = Empty()
pose_o.model_name = "unit_box"

def heron(a):
	video_capture = cv2.VideoCapture(a, cv2.CAP_V4L2)
	video_capture.release()
	video_capture = cv2.VideoCapture(a, cv2.CAP_V4L2)

	if not video_capture.isOpened():
		print("Cannot open camera 2")
		exit()
	while True:
		ret, frame = video_capture.read()
		if ret:
			code = decode(frame)
			for qrcode in code:
				print('0')
	return 0

camera1 = threading.Thread(target=heron, args=(4,))
camera2 = threading.Thread(target=heron, args=(0,))
camera3 = threading.Thread(target=heron, args=(2,))

camera1.start()
camera2.start()
camera3.start()
