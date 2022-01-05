import numpy as np
import math
import cv2

def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).

def TF(rvecs, tvecs):
	tf = np.zeros((4,4), dtype= float)
	rotation_matrix = np.transpose(cv2.Rodrigues(rvecs)[0]) 
	tf[0:3, 0:3] = rotation_matrix
	tf[3][3] = 1
	tf[0:3, 3:4] = np.dot(-rotation_matrix, tvecs)/1000
	return tf

def eulerAnglesToRotationMatrix(R):
    r = np. array([0, 0, 0])
    if(isRotationMatrix(R)):
        r, _ = cv2.Rodrigues(R)
    return np.array([r[0], r[1], r[2]])


