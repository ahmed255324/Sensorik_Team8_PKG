from math import pi
import numpy as np
import cv2
import tabelle

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).


def TF(tvecs):
	tf = np.zeros((4,4), dtype= float)
	tf[0:3, 0:3] = np.eye(3)
	tf[3][3] = 1
	tf[0:3, 3:4] = tvecs/1000
	return tf



def Angle(win):
    if(win in tabelle.win_0):
        return 0
    elif(win in tabelle.win_30):
        return pi/6
    elif(win in tabelle.win_60):
        return pi/3
    elif(win in tabelle.win_90):
        return pi/2
    elif(win in tabelle.win_120):
        return 2*pi/3
    elif(win in tabelle.win_150):
        return 5*pi/6
    elif(win in tabelle.win_180):
        return pi
    elif(win in tabelle.win__30):
        return -pi/6
    elif(win in tabelle.win__60):
        return -pi/3
    elif(win in tabelle.win__90):
        return -pi/2
    elif(win in tabelle.win__120):
        return -2*pi/3
    elif(win in tabelle.win__150):
        return -5*pi/6
    else:
        print (win," nicht definiert!!")
        return 0



