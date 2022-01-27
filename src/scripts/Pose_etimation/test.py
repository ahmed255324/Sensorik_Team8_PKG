#!/usr/bin/env python
import cv2
from _thread import start_new_thread
import threading
from pyzbar.pyzbar import decode

from picamera.array import PiRGBArray
from picamera import PiCamera

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array
# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)

def heron(a):
    video_capture = cv2.VideoCapture(a, cv2.CAP_V4L2)
    if not video_capture.isOpened():
        print("Cannot open camera 2")
        exit()
    while True:
        ret, frame = video_capture.read()
        if ret:
            code = decode(frame)
            for qrcode in code:
                print(a)
    return 0

camera1 = threading.Thread(target=heron, args=(0,))

camera1.start()
c = print("Eingabe.")