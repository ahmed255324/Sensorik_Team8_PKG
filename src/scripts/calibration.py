#!/usr/bin/env python 

from pyzbar.pyzbar import decode
import numpy as np
import cv2


#video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(2)
#video_capture3 = cv2.VideoCapture(4)

i = 1

while(True):

	#ret1, frame1 = video_capture1.read()
	ret2, frame2 = video_capture2.read()
	#ret3, frame3 = video_capture3.read()


	#code1 = decode(frame1)
	#code2 = decode(frame2)
	#code3 = decode(frame3)
	cv2.imshow("USB-cam-1", frame2)

	cv2.imwrite('Usb_cam_calabration_1/Bild_'+str(i)+'.png', frame2)
	i = i + 1
	#cv2.imshow("Frame3",frame3)
	if cv2.waitKey(1000) & 0xFF == ord('q'):
		break

#video_capture1.release()
video_capture2.release()
#video_capture3.release()
cv2.destroyAllWindows()