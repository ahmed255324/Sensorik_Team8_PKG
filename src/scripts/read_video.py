#!/usr/bin/env python 

from pyzbar.pyzbar import decode
import numpy as np
import cv2


#video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(2)
#video_capture3 = cv2.VideoCapture(4)

while(True):
	#ret1, frame1 = video_capture1.read()
	ret2, frame2 = video_capture2.read()
	#ret3, frame3 = video_capture3.read()

	#code1 = decode(frame1)
	code2 = decode(frame2)
	#code3 = decode(frame3)
	for qrcode in code2:
		print(qrcode.polygon)
	#rect_foto1 = cv.rectangle(frame1, code1.rect     ,(510,128),(0,255,0),3)
	#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#frame = cv2.resize(frame, (0,0), fx=0.5,fy=0.5)
	#cv2.line(frame,(0,0),(511,511),(255,0,0),5)
	#cv2.imshow("Frame1",frame1)
	cv2.imshow("Frame2",frame2)
	#cv2.imshow("Frame3",frame3)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#video_capture1.release()
video_capture2.release()
#video_capture3.release()
cv2.destroyAllWindows()

