#!/usr/bin/env python3
#pygame in order to capture image from webcam
#PIL in order to draw camera mane and date time on the photo
#telegram_send in order to send captured images to telegram
import time
import pygame.camera
import pygame.image
import telegram_send
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pygame.locals import *
from pathlib import Path        # python 3.5+
import socket
from config import *            # This way you can use global variables from config.py directly

REMOTE_SERVER = "www.google.com"
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",25)
COLOR_FONT = (0, 255, 0)
homedir = str(Path.home())
img_path = homedir+"/remotecam/photo.jpg"     # Full path NEEDED to DAEMON. See remotecam.sh !!!
pygame.camera.init()
cams = []
MSG = MSG_START
failed = False
timefailed = ""
# Send a message to the Telegram bot you have created
telegram_send.send(messages=[MSG])
list_cameras=pygame.camera.list_cameras()

while True:
    if failed == True:
		# Wait for 60 seconds and try againg to send snapshot/s
        time.sleep(60)
    else:
        time.sleep(INTERVAL)
    # Capture images from every connected webcam
    for cam_name in list_cameras:
        cam = pygame.camera.Camera(cam_name,(640, 480))
        # Camera shot
        timeimg = time.strftime("%e %b %Y %T")
        try:
            cam.start()
        except:
            continue   
        img = cam.get_image()
        pygame.image.save(img, homedir+"/remotecam/photo.png")    # With expansion tilde is expanded to "/home/username/dir_name/"
        imgPIL = Image.open(homedir+"/remotecam/photo.png")
        draw = ImageDraw.Draw(imgPIL)
        draw.text((10,450), (cam_name[-6:]),COLOR_FONT,font=font)
        draw.text((350, 450),timeimg,COLOR_FONT,font=font)
        imgPIL.save(homedir+"/remotecam/photo.jpg")
        cam.stop()
        with open(img_path, "rb") as f:
            # Test internet connection
            try:
                host = socket.gethostbyname(REMOTE_SERVER)
                s = socket.create_connection((host, 80), 2)
            except:
                timefailed = timefailed + "-" + timeimg
                MSG = MSG_FAILED+timefailed
                failed = True
                continue
            if failed == True:
                # Now internet connection is available again.
                # Before sending capptured images, send a warning message displaying the timestamps of internet connection failures.
                telegram_send.send(messages=[MSG])  
            failed = False
            telegram_send.send(images=[f])

pygame.camera.quit()
