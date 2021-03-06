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

pygame.camera.init()
  
# make the list of all available cameras
camlist = pygame.camera.list_cameras()

cam1 = pygame.camera.Camera(camlist[4], (640, 480))
cam2 = pygame.camera.Camera(camlist[0], (640, 480))
cam3 = pygame.camera.Camera(camlist[2], (640, 480))

cam1.start()
cam2.start()
cam3.start()

a = 190

cameraMatrix_2 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/cameraMatrix_2.csv", delimiter=',')
cameraMatrix_3 = np.genfromtxt("/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/cameraMatrix_3.csv", delimiter=',')


dist_2 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_2/dist_2.csv', delimiter=',')
dist_3 = np.genfromtxt('/home/ubuntu/catkin_ws/src/Sensorik_Team8_PKG/src/scripts/Usb_cam_calabration_3/dist_3.csv', delimiter=',')

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objectPoints = np.array([[-a/2, a/2, 0], [-a/2, -a/2, 0], [a/2, -a/2, 0], [a/2, a/2, 0]], dtype=np.float32)
objectPoints = np.reshape(objectPoints, (4,3,1))
points = np.array((4,2))

tf_2 = np.zeros((4,4))
tf_3 = np.zeros((4,4))

x = 0.0
y = 0.0

cam_2 = 1
cam_3 = 10
win = 0

while(not rospy.is_shutdown()):
    image = cam2.get_image()
    view = pygame.surfarray.array3d(image)
    view = view.transpose([1, 0, 2])
    frame2 = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
    code2 = decode(frame2)
    for qrcode2 in code2:
        barcodeData_2 = int(qrcode2.data.decode("utf-8"))
        points = np.array(code2[0].polygon, np.float32)
        if((4,2) == np.shape(points)):
            _, _, tvecs_2 = cv2.solvePnP(objectPoints, np.reshape(points, (4,2,1)), cameraMatrix_2, dist_2, flags=cv2.SOLVEPNP_P3P)
            if tvecs_2 is not None:
                tf_2[2] = tf_2[2] + 0.1
                tf_2 = np.dot(tabelle.qrcode_tf[barcodeData_2-1], funktionen.TF(tvecs_2))
                if(barcodeData_2 >= 1 and barcodeData_2 < 20):
                    y = tf_2[1][3]
                else:
                    x = tf_2[0][3]
        win = win + barcodeData_2 * cam_2
 
    image = cam3.get_image()
    view = pygame.surfarray.array3d(image)
    view = view.transpose([1, 0, 2])
    frame3 = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
    code3 = decode(frame3)
    for qrcode3 in code3:
        barcodeData_3 = int(qrcode3.data.decode("utf-8"))
        points = np.array(code3[0].polygon, np.float32)
        if((4,2) == np.shape(points)):
            _, _, tvecs_3 = cv2.solvePnP(objectPoints, np.reshape(points, (4,2,1)), cameraMatrix_3, dist_3, flags=cv2.SOLVEPNP_P3P)
            if tvecs_3 is not None:
                tf_3[2] = tf_3[2] + 0.1
                tf_3 = np.dot(tabelle.qrcode_tf[barcodeData_3-1], funktionen.TF(tvecs_3))
                if(barcodeData_3 >= 1 and barcodeData_3< 20):
                    x = tf_3[0][3]
                else:
                    y = tf_3[1][3]
        win = win + barcodeData_3 * cam_3

    if(code3 or code2):
        pose_o.pose.position.x = x
        pose_o.pose.position.y = y
        print(x, y)
        pose_o.pose.position.z = 0.0
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

cam2.stop()
cam3.stop()