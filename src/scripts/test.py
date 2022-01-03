#!/usr/bin/env python

import cv2
import numpy as np
from pyzbar.pyzbar import decode

video_capture1 = cv2.VideoCapture(2)

while(True):
    ret1, image = video_capture1.read()
    # Pattern points in 2D image coordinates
    code1 = decode(image)
	
    for qrcode1 in code1:
        print(qrcode1)
    cv2.imshow("image",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

video_capture1.release()
cv2.destroyAllWindows()