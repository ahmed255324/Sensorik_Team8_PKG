import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data('2')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

img.save("qrcode.png")

import cv2 as cv
import numpy as np

im = cv.imread('qrcode.png')


det = cv.QRCodeDetector()


decoded_info, points, _ = det.detectAndDecode(im)


print(decoded_info)
print(points)


print(type(points))
