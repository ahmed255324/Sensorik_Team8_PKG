import qrcode
from fpdf import FPDF

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

images.extend(sorted(glob.glob('*.png')))
 

# Create instance of FPDF class
pdf=FPDF('P','mm','A4')
# Add new page. Without this you cannot create the document.
 
# Smaller font for image captions
pdf.set_font('Arial','',100)
 
# Loop through the image list and position
# them with their caption one below the other
i = 1
for image in images:
    pdf.add_page()
    # Setting image width to half the page and
    # height to 1/4th of the page
    pdf.image(image, x = 2, y = 2 , w=pdf.w/1.02, h=pdf.w/1.02)
 
# output content into a file ('F')
pdf.output('qr-Cods.pdf','F')