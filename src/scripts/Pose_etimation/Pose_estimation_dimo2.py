import numpy as np
import cv2 as cv

# Load previously saved data
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



criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
axisBoxes = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

video_capture = cv.VideoCapture(0, cv.CAP_V4L2)

while not(cv.waitKey(1) & 0xFF == ord('q')):
    ret1, frame = video_capture.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (9,6),None)

    if ret == True:
        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1), criteria)

        # Find the rotation and translation vectors.
        ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)

        # Project 3D points to image plane
        imgpts, jac = cv.projectPoints(axisBoxes, rvecs, tvecs, mtx, dist)

        img = drawBoxes(frame,corners2,imgpts)
        cv.imshow('img',img)
    else:
        cv.imshow('img',frame)

video_capture.release()
cv.destroyAllWindows()