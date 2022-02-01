import io
import qrcode
from fpdf import FPDF
import base64
from PIL import Image
import cv2
import numpy as np
import io
import re

# Take in base64 string and return cv image
def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=0,
)

for i in range(1, 31):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(i)
    img = qr.make_image(fill_color="black", back_color="white")
    name = str(i)+".png"
    img.save(name)

 
# Import glob module to find all the files matching a pattern
import glob
 
# Image extensions
image_extensions = ("*.png", "*.jpg", "*.gif")
 
# This list will hold the images file names
images = []
 
# Build the image list by merging the glob results (a list of files)
# for each extension. We are taking images from current folder.

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

images.extend(sorted(glob.glob('*.png'), key=numericalSort))
 

# Create instance of FPDF class
pdf=FPDF('P','mm','A4')
# Add new page. Without this you cannot create the document.
 
# Smaller font for image captions
pdf.set_font('Arial','',100)

det = cv2.QRCodeDetector()


 
# Loop through the image list and position
# them with their caption one below the other
i = 1
for image in images:
    pdf.add_page()
    # Setting image width to half the page and
    # height to 1/4th of the page
    pdf.image(image, x = 2, y = 2 , w=pdf.w/1.02, h=pdf.w/1.02)

    pdf.ln(250.25)
    pdf.cell(4.0,1.0, str(i))
    i = i + 1
 
# output content into a file ('F')
pdf.output('qr-Cods.pdf','F')