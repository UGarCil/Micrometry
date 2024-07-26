import pygame 
import os 
import cv2 
import argparse
from os.path import join as jn
from conditions import *

########################### ARGPARSE arguments ###################################
parser = argparse.ArgumentParser(description='Line measurement tool')
parser.add_argument("--ci", default=0,type=int,help='Index of the camera (for multiple camera devices connected)')
parser.add_argument("--res", default=0.6,type=float,help="determine the dimensions of the window, from 0 to 1 (float)")
parser.add_argument("--kc", default=1,type=int,help="Determine whether to take the classes from template (0) or previous sessions (1)")
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
W = int(display_info.current_w*args.res)
H = int(W*cameraRatio)

SCREEN = (W,H)
display = pygame.display.set_mode(SCREEN)
# Initialize webcam




# DD. SAVEPATH 
# savePath = str
# interp. the location of the file that will store the program's output
savePath = jn(os.path.dirname(__file__),"output.txt")


# DD. MOUSE_POSITION
# mousePos = (int,int)
# interp. the current position of the mouse, defined by user
mousePos = pygame.mouse.get_pos()

# DD. VALID_LINE_NAMES
# validLineNames = [str, ...]
# interp. a collection of valid names for the file name given to a measurement or label
validLineNames = [_ for _ in "abcdefghiklmnopqrstuvwxyz"] + [_ for _ in "abcdefghiklmnopqrstuvwxyz".upper()] + [_ for _ in "_.-:;/\\\t\n"] + [_ for _ in "0123456789"]


# DD. CLASSES
# classes = []
# interp. a collection of class names
classes = []

# Determine which file to use to read the classes
if os.path.exists("./labels/classes.txt") and bool(args.kc):
    targetClassFile = "./labels/classes.txt"
else:
    targetClassFile = "./predefined_classes.txt"

with open(targetClassFile,"r") as file:
    file = file.readlines()
    classes = [line.strip() for line in file]


# DD. IMAGE_FILE_EXTENSIO
# ife = str
# interp. a file extension to save the images
# One of:
#   -   .jpg
#   -   .png
ife = ".jpg"