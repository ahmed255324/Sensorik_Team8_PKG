import pygame
import pygame.camera
  
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
  
# if camera is not detected the moving to else part
else:
    print("No camera on current device")