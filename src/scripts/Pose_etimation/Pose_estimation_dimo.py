import numpy as np
import cv2 as cv
from pyzbar.pyzbar import decode


mtx = np.genfromtxt("src/scripts/cameraMatrix.csv", delimiter=',')
dist = np.genfromtxt('src/scripts/dist.csv', delimiter=',')

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 10)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 10)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 10)
    return img


def drawBoxes(img, corners, imgpts):

    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

objectPoints = np.random.random((4,3,1))
imagePoints = np.random.random((4,2,1))

a = 120

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objectPoints[0] = [[-a/2], [a/2], [0]]
objectPoints[1] = [[-a/2], [-a/2], [0]]
objectPoints[2] = [[a/2], [-a/2], [0]]
objectPoints[3] = [[a/2], [a/2], [0]]

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
axisBoxes = np.float32([[0,0,0], [0,20,0], [20,20,0], [20,0,0],
                   [0,0,-20],[0,20,-20],[20,20,-20],[20,0,-20] ])

video_capture = cv.VideoCapture(0, cv.CAP_V4L2)

while not(cv.waitKey(1) & 0xFF == ord('q')):
    ret1, frame = video_capture.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    code = decode(gray)

    if code:
        points = np.array(code[0].polygon, np.int32)
        imagePoints[0] = [[points[0][0]], [points[0][1]]]
        imagePoints[1] = [[points[1][0]], [points[1][1]]]
        imagePoints[2] = [[points[2][0]], [points[2][1]]]
        imagePoints[3] = [[points[3][0]], [points[3][1]]]
        
        # Find the rotation and translation vectors.
        ret, rvecs, tvecs = cv.solvePnP(objectPoints, imagePoints, mtx, dist)

        # Project 3D points to image plane
        imgpts, jac = cv.projectPoints(axisBoxes, rvecs, tvecs, mtx, dist)

        img = drawBoxes(frame,objectPoints,imgpts)
        cv.imshow('img',img)
    else:
        cv.imshow('img',frame)
    
cv.destroyAllWindows()
video_capture.release()