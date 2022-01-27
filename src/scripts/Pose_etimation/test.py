#!/usr/bin/env python
import cv2
from _thread import start_new_thread
import threading
from pyzbar.pyzbar import decode

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