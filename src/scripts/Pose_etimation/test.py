#!/usr/bin/env python

import cv2 
from pyzbar.pyzbar import decode
from sympy import true
import cv


video_capture1 = cv2.VideoCapture(2, cv2.CAP_V4L2)
fps = int(video_capture1.get(5))
print("fps:", fps)

video_capture2 = cv2.VideoCapture(4, cv2.CAP_V4L2)
fps = int(video_capture2.get(5))
print("fps:", fps)

video_capture3 = cv2.VideoCapture(6, cv2.CAP_V4L2)
fps = int(video_capture3.get(5))
print("fps:", fps)

while(true):

	ret1, frame1 = video_capture1.read()
	if ret1:
		code1 = decode(frame1)
		for qrcode1 in code1:
			print('1')

	ret2, frame2 = video_capture2.read()
	if ret2:
		code2 = decode(frame2)
		for qrcode2 in code2:
			print('2')

	ret3, frame3 = video_capture3.read()
	if ret3:
		code3 = decode(frame3)
		for qrcode3 in code3:
			print('3')

	
video_capture1.release()
video_capture2.release()
video_capture3.release()