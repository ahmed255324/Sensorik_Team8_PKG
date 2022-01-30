import pygame
import pygame.camera
import cv2
  
# initializing  the camera
pygame.camera.init()
  
# make the list of all available cameras
camlist = pygame.camera.list_cameras()
  
# if camera is detected or not

print(len(camlist))
if camlist:
  
    # initializing the cam variable with default camera
    cam_1 = pygame.camera.Camera(camlist[0], (640, 480))

    # opening the camera
    cam_1.start()
  
    # capturing the single image
    image = cam_1.get_image()
  
    # saving the image
    view = pygame.surfarray.array3d(image)

#  convert from (width, height, channel) to (height, width, channel)
    view = view.transpose([1, 0, 2])

    #  convert from rgb to bgr
    img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR) 

    cv2.imshow("cv image", img_bgr)

    cv2.waitKey(3000)
    
# if camera is not detected the moving to else part
else:
    print("No camera on current device")
import tabelle

print(tabelle.qrcode_tf[int(1)-1][0][3])