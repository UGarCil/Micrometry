# This algorithm is designed to facilitate the creation of dataset for machine learning algorithms. The program creates the images and places them into their 
# folders, where the folders are created using a prefix (label) chosen by the user.


# MODULES

import pygame
import os
from Button import Button
from constants import *
from TextBox import Textbox
from Text import TextAlarm
from PictureManager import saveImage
from MOG import mog3
from Box import Box
import numpy as np

############### DD  ###############
# DD. USER_WANTS_PREFIX
# userWantsTypePrefix = bool
# interp. whether the user wants to manually type a prefix for each image taken
userWantsTypePrefix = True

# DD. VALID_LINE_NAMES
# validLineNames = [str, ...]
# interp. a collection of valid names for the file name given to a measurement
validLineNames = [_ for _ in "abcdefghiklmnopqrstuvwxyz"] + [_ for _ in "abcdefghiklmnopqrstuvwxyz".upper()] + [_ for _ in "_.-:;/\\\t\n"] + [_ for _ in "0123456789"]


# DD. BUTTON
# button = Button()
# interp. a button that will be insterted into the panel
buttonSB  = Button(W//32,H//32,W//10,H/24,"SCALEBAR",text_size=14)
buttonSB.original_color = (255,100,100)
# buttonClear  = Button(W//32,H//32 * 3,W//10,H/24,"CLEAR")
buttonMeasure = Button(W//32,H//32 * 1,W//10,H/24,"SELECT")
buttonMeasure.original_color = (100,255,100)

buttonSetPath = Button(W//32,H//32 * 5,W//10,H/24,"SET PATH..",text_size=14)
buttonPHOTO = Button(W//32,H//32 * 7,W//10,H/24,"PICTURE",text_size=14)
buttonFREEZE = Button(W//32,H//32 * 3,W//10,H/24,"FREEZE",text_size=14)
buttonMOG = Button(W//32,H//32 * 5,W//10,H/24,"EDGE MODE",text_size=14,text_color="white")
buttonMOG.original_color = (0,0,0)

buttonPREFIX = Button(W//32,H//32 * 7,W//10,H/24,"SET PREFIX",text_size=14,text_color="white")
buttonPREFIX.original_color = (100,100,255)

# DD. LIST_OF_BUTTONS
# interp. a collection of Buttons to determine animation and functions
lob = [buttonMeasure,buttonFREEZE,buttonMOG,buttonPREFIX]

# DD. PRESSING_SCREEN_BUTTON
# isPressingScreenButton = bool
# interp. whether the left button mouse is being held down or not
isPressingScreenButton = False

# DD. IS_IN_MEASURE_MODE
# measureMode = bool
# interp. whether the user is currently taking measurements or not
measureMode = False

# DD. IS_IN_SCALEBAR_MODE
# scalebarMode = bool
# a subcondition to IS_IN_MEASURE_MODE being True. It determines whether in line or scalebar mode
scalebarMode = False

# DD. IS_IN_BOX_MODE
# boxMode = bool
# interp. whether or not the program is taking a picture
boxMode = False


# DD. TEXT_BOX_OBJ
# text_box = Textbox()
# interp. a box to declare the value of a SCALEBAR_OBJ
text_box = Textbox(0,0,"red")
text_box_SAVEDATA = Textbox(0,0,"green",prefix="Name: ")
text_box_SAVEDATA.isACTIVE = False
text_box_PREFIX = Textbox(0,0,"green",prefix="Name: ")
text_box_PREFIX.isACTIVE = False

# DD. TEXT_ALARM
# text_alarm = TextAlarm()
# interp. a message that appears at the bottom of the screen notifying the user about warnings
text_alarm = TextAlarm("",0,0,16)


# DD. CV2_FREEZE
# cv2Freezed = bool
# interp. whether the user wants to freeze the camera view or not
cv2Freezed = False

# DD. MOG_ACTIVE
# MOGMode = bool
# interp. determines the use of Edge detection mode
MOGMode = False

# DD. BOX
# box = Box()
# interp. a square that will delimit the area that will be sampled to create an input to a dataset
box = Box(0,0)


# DD. PREFIX
# prefix = str
# interp. the prefix selected by the user to name images
prefix = ""

# CODE
# FD. updateCV2Frames()
# purp. create a surface class object with the feed from the webcam
def updateCV2Frames():
    global frame,surface
    global first,idx
    _,frame = cap.read()
    if not cv2Freezed:
        surface = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = cv2.rotate(surface, cv2.ROTATE_90_COUNTERCLOCKWISE)
        surface = cv2.flip(surface,0)
        surface = cv2.resize(surface, (H,W))  #HEIGHT AND WIDTH get flipped because or the counterclockwise rotation
        if MOGMode:
            surface = mog3(surface)
        surface = pygame.surfarray.make_surface(surface)
    display.blit(surface,(0,0))


def draw():
    display.fill("black")
    updateCV2Frames()
    for button in lob:
        if not measureMode:
            button.draw()
    if measureMode and boxMode:
        box.draw()
        text_box_SAVEDATA.draw()
    # text_box.draw()
    if measureMode and not boxMode:
        text_box_PREFIX.draw()
    text_alarm.draw_text()
    pygame.display.flip()




    
    
    
# FD. updateUserInput()
# purp. Read and change parameters based on the interaction with the main user
def updateUserInput():
    global prefix
    global isPressingScreenButton
    global measureMode
    global scalebarMode
    global text_alarm
    global text_box_SAVEDATA
    global boxMode
    global userWantsTypePrefix
    global box
    global cv2Freezed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # evaluate left mouse button pressed
            if event.button == 1: 
                isPressingScreenButton = True
                if measureMode and boxMode:
                    box.onMouseDown()
            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                isPressingScreenButton = False
                
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                measureMode = False
                boxMode = False

        
        if event.type == pygame.KEYDOWN:
            if text_box_SAVEDATA.isACTIVE and boxMode:
                # The tag given to a measurement can include any letter, number and some special characters
                if event.unicode.isalnum() or event.unicode in validLineNames:
                    text_box_SAVEDATA.input_text += event.unicode
                # Handle backspace to delete characters
                elif event.key == pygame.K_BACKSPACE:
                    text_box_SAVEDATA.input_text = text_box_SAVEDATA.input_text[:-1]
                # Handle return/enter to finish input
                elif event.key == pygame.K_RETURN:
                    if measureMode:
                        if len(text_box_SAVEDATA.input_text) >0:
                            text_box_SAVEDATA.isACTIVE = False; draw()
                            pygame.display.flip()
                            saveImage(box,text_box_SAVEDATA.input_text)
                        else:
                            text_alarm = TextAlarm("Please enter at least one character",W//2,H-80,16,2000)
                        text_box_SAVEDATA.isACTIVE = False
                        # boxMode = False 
                        # measureMode = False
                        box = Box(0,0)
                        
            # Evaluate if the prefix is active as well
            elif text_box_PREFIX.isACTIVE and not boxMode:
                # The tag given to a measurement can include any letter, number and some special characters
                if event.unicode.isalnum() or event.unicode in validLineNames:
                    text_box_PREFIX.input_text += event.unicode
                # Handle backspace to delete characters
                elif event.key == pygame.K_BACKSPACE:
                    text_box_PREFIX.input_text = text_box_PREFIX.input_text[:-1]
                # Handle return/enter to finish input
                elif event.key == pygame.K_RETURN:
                    if measureMode:
                        if len(text_box_PREFIX.input_text) >0:
                            # if not os.path.exists(savePath):
                            prefix = text_box_PREFIX.input_text
                        else:
                            text_alarm = TextAlarm("Please enter at least one character",W//2,H-80,16,2000)
                        text_box_PREFIX.isACTIVE = False
                        # scalebarMode = False 
                        measureMode = False
                        userWantsTypePrefix = False
                        print(prefix)
            
            # Listen for shortcut keys
            if not text_box_PREFIX.isACTIVE and not text_box_PREFIX.isACTIVE:
                # enter/leave Freeze mode
                if event.key == pygame.K_SPACE:
                    for button in lob:
                        if button.name == "FREEZE":
                            # use the resized global variable surface from the function updateCVFrames() to take a picture
                            button.name = "UNFREEZE"
                            cv2Freezed = True
                            button.updateName()
                        elif button.name == "UNFREEZE":
                            button.name = "FREEZE"
                            cv2Freezed = False
                            button.updateName()
            
                if event.unicode == "s" and not boxMode:
                    for button in lob:
                        if button.name == "SELECT":
                            measureMode = True
                            boxMode = True
                            box = Box(0,0)


# FD. updateButtons()
# purp. change the colors of the buttons, and handle switches controlling the program's modes
def updateButtons():
    global measureMode
    global isPressingScreenButton
    global scalebarMode
    global scalebar
    global spline
    global savePath
    global cv2Freezed
    global MOGMode
    global box
    global text_box_PREFIX
    global userWantsTypePrefix
    global boxMode
    for button in lob:
        # if the cursor hovers the button, change its color
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            # evaluate if user wants to click on a button
            if isPressingScreenButton and button.ready:
                button.color = (100,100,100)
                # if button.name == "SCALEBAR":
                #     measureMode = True
                #     scalebarMode = True 
                #     scalebar = Scalebar()
                #     # scalebar.resetTimer()
                if button.name == "SELECT":
                    measureMode = True
                    boxMode = True
                    box = Box(0,0)
                # elif button.name == "SET PATH..":
                #     savePath = save_as_dialog()
                # elif button.name == "PICTURE":
                #     # use the resized global variable surface from the function updateCVFrames() to take a picture
                #     takePic(surface,savePath)
                elif button.name == "FREEZE":
                    # use the resized global variable surface from the function updateCVFrames() to take a picture
                    button.name = "UNFREEZE"
                    cv2Freezed = True
                    button.updateName()
                elif button.name == "UNFREEZE":
                    # use the resized global variable surface from the function updateCVFrames() to take a picture
                    button.name = "FREEZE"
                    cv2Freezed = False
                    button.updateName()
                elif button.name == "EDGE MODE":
                    button.name = "RGB MODE"
                    MOGMode = True
                    button.updateName()
                elif button.name == "RGB MODE":
                    button.name = "EDGE MODE"
                    MOGMode = False
                    button.updateName()
                elif button.name == "SET PREFIX":
                    text_box_PREFIX = Textbox(W//2, H - 30,"black",prefix="Prefix: ")
                    measureMode = True
                    boxMode = False
                # reset the 
                button.resetRecoil()
                    
            else:
                button.color = (200,200,200)
        else:
            button.color = button.original_color


    
def update():
    global measureMode
    global text_box_SAVEDATA
    global box
    updateUserInput()   # Listen to user input
    if not measureMode: updateButtons()     # update button colors and program modes

    # if the box has entered the last stage, prompt the input text if decided by the user and save the image with its prefix
    # Once the box has been defined, put it in standby with the boolean waitingForPrefix. Once user fills prefix, a new BOX is created
    if box.stage3 and not box.waitingForPrefix:
        # Update the position of the coordinates of the box by locating the top left corner as the position x,y
        box.updatePointOfOrigin()
        box.waitingForPrefix = True
        if userWantsTypePrefix:
            text_box_SAVEDATA = Textbox(W//2, H - 30,"black",prefix="Prefix: ")
        # if the user automated prefix designation, 
        else:
            draw()
            pygame.display.flip()
            saveImage(box,prefix)
            box = Box(0,0)
            box.waitingForPrefix = False
            
        
        

    
    
while True:
    draw()
    update()