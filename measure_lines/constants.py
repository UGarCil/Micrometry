import pygame 
import os 
import cv2 
import argparse
from os.path import join as jn

########################### ARGPARSE arguments ###################################
parser = argparse.ArgumentParser(description='Line measurement tool')
parser.add_argument("--ci", default=0,type=int,help='Index of the camera (for multiple camera devices connected)')
args = parser.parse_args()

##################################################################################
pygame.init()
display_info = pygame.display.Info()

# Determine the width and height ratio of the camera
cap = cv2.VideoCapture(args.ci)
cameraW = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cameraH = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cameraRatio = cameraH/cameraW #what proportion of the width is the height (e.g. for 1920 x 1080, it's 0.56)


# Make the dimensions of the window 80% of the user's screen
W = int(display_info.current_w*0.6)
H = int(W*cameraRatio)

SCREEN = (W,H)
display = pygame.display.set_mode(SCREEN)
# Initialize webcam




# DD. SAVEPATH 
# savePath = str
# interp. the location of the file that will store the program's output
savePath = jn(os.path.dirname(__file__),"output.txt")

