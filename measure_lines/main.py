# This algorithm is designe to facilitate the analysis of biological data when using a microscope and a digital camera.
# It allows its users to make measurements of structures in real time, as long as there is a notion of length (i.e. scalebar is known)
# to calibrate the model.


# MODULES

import pygame
import os
from Button import Button
from constants import *
from Scalebar import Scalebar, Line
from TextBox import Textbox
from Text import TextAlarm, Text
from tkinter_utils import save_as_dialog,get_formatted_timestamp
import time
from PictureManager import takePic


############### DD  ###############


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
buttonMeasure = Button(W//32,H//32 * 3,W//10,H/24,"LINE")
buttonMeasure.original_color = (100,255,100)

buttonSetPath = Button(W//32,H//32 * 5,W//10,H/24,"SET PATH..",text_size=14)
buttonPHOTO = Button(W//32,H//32 * 7,W//10,H/24,"PICTURE",text_size=14)

# DD. LIST_OF_BUTTONS
# interp. a collection of Buttons to determine animation and functions
lob = [buttonSB,buttonMeasure,buttonSetPath,buttonPHOTO]

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

# DD. SCALEBAR_OBJ
# scalebar = Scalebar()
# interp. parameters and points representing the scalebar
scalebar = Scalebar()

# DD. TEXT_BOX_OBJ
# text_box = Textbox()
# interp. a box to declare the value of a SCALEBAR_OBJ
text_box = Textbox(0,0,"red")
text_box_line = Textbox(0,0,"green",prefix="Name: ")

# DD. TEXT_ALARM
# text_alarm = TextAlarm()
# interp. a message that appears at the bottom of the screen notifying the user about warnings
text_alarm = TextAlarm("",0,0,16)

# DD. LINE
# line = Line()
# interp. a segment created to measure the distance between two points
line = Line()

# CODE
# FD. updateCV2Frames()
# purp. create a surface class object with the feed from the webcam
def updateCV2Frames():
    global frame,surface
    global first,idx
    _,frame = cap.read()
    surface = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    surface = cv2.rotate(surface, cv2.ROTATE_90_COUNTERCLOCKWISE)
    surface = cv2.flip(surface,0)
    surface = cv2.resize(surface, (H,W))  #HEIGHT AND WIDTH get flipped because or the counterclockwise rotation
    surface = pygame.surfarray.make_surface(surface)
    display.blit(surface,(0,0))


def draw():
    display.fill("black")
    updateCV2Frames()
    for button in lob:
        if not measureMode:
            button.draw()
    if measureMode:
        if scalebarMode:
            scalebar.draw()
        else:
            line.draw(scalebar)
    text_box.draw()
    text_box_line.draw()
    text_alarm.draw_text()
    pygame.display.flip()


# FD. updateDisplay_forImageTaking()
# purp. render a screen without buttons, while preserving the line draw elements
def updateDisplay_forImageTaking():
    updateCV2Frames()
    if measureMode:
        if scalebarMode:
            scalebar.draw()
        else:
            line.draw(scalebar)
    text_box_line.draw()
    text_alarm.draw_text()
    pygame.display.flip()
    
# FD. updateScaleBar()
# purp. create a line between two points representing the width of the scalebar
def updateScalebar():
    global text_box
    if not scalebar.firstClick:
        if not scalebar.isPt1Done:
            scalebar.pt1 = pygame.mouse.get_pos()
            scalebar.isPt1Done = True
            # scalebar.follow_the_mouse = True
        else:
            if not scalebar.isPt2Done:
                scalebar.pt2 = pygame.mouse.get_pos()
                scalebar.isPt2Done = True
                #process the scalebar information
                text_box = Textbox(scalebar.pt2[0],scalebar.pt2[1]-16,"red")
    else:
        scalebar.firstClick = False
        
# FD. updateLine()
# purp. create a line between two points representing a measurement, given a valid SCALEBAR
def updateLine():
    global text_box_line
    if not line.firstClick:
        if not line.isPt1Done:
            line.pt1 = pygame.mouse.get_pos()
            line.isPt1Done = True
        else:
            if not line.isPt2Done:
                line.isPt2Done = True
                text_box_line = Textbox(W//2, H-32,"green",prefix="Name: ")
                
                
                
    else:
        line.firstClick = False

# FD. updateUserInput()
# purp. Read and change parameters based on the interaction with the main user
def updateUserInput():
    global isPressingScreenButton
    global measureMode
    global scalebarMode
    global text_alarm
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # evaluate left mouse button pressed
            if event.button == 1: isPressingScreenButton = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                isPressingScreenButton = False
                if measureMode:
                    if scalebarMode: updateScalebar()
                    else: updateLine()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                measureMode = False
                text_box.isACTIVE=False
                text_box_line.isACTIVE = False
                scalebarMode = False 
        
        if event.type == pygame.KEYDOWN:
            if text_box.isACTIVE:
                # Check if the key is a number, period, or backspace
                if event.unicode.isdigit() or event.unicode == '.':
                    # Check if the input text already contains a dot
                    if event.unicode == '.' and '.' not in text_box.input_text or event.unicode.isdigit():
                        text_box.input_text += event.unicode
                    # # Check if it's a digit
                    # elif event.unicode.isdigit():
                    #     text_box.input_text += event.unicode
                # Handle backspace to delete characters
                elif event.key == pygame.K_BACKSPACE:
                    text_box.input_text = text_box.input_text[:-1]
                # Handle return/enter to finish input
                elif event.key == pygame.K_RETURN:
                    if measureMode and scalebarMode:
                        try:
                            text_box.value = float(text_box.input_text)
                            scalebar.calibrateScalebar(text_box.value)
                        except:
                            text_alarm = TextAlarm("Please enter a valid numerical value",W//2,H-30,16,2000)
                        text_box.isACTIVE = False
                        scalebarMode = False 
                        measureMode = False
                        
            elif text_box_line.isACTIVE:
                # The tag given to a measurement can include any letter, number and some special characters
                if event.unicode.isalnum() or event.unicode in validLineNames:
                    text_box_line.input_text += event.unicode
                # Handle backspace to delete characters
                elif event.key == pygame.K_BACKSPACE:
                    text_box_line.input_text = text_box_line.input_text[:-1]
                # Handle return/enter to finish input
                elif event.key == pygame.K_RETURN:
                    if measureMode and not scalebarMode:
                        if len(text_box_line.input_text) >0:
                            # if not os.path.exists(savePath):
                            with open(savePath,"a") as file:
                                file.write(f"{text_box_line.input_text}\t{round(line.value,5)}\t{get_formatted_timestamp()}\n")
                        else:
                            text_alarm = TextAlarm("Please enter at least one character",W//2,H-80,16,2000)
                        text_box_line.isACTIVE = False
                        scalebarMode = False 
                        measureMode = False
            
            if not text_box.isACTIVE:
                if event.unicode == "p":
                    updateDisplay_forImageTaking()
                    # Instead of using the resized global variable pygame object surface from the function updateCVFrames()
                    # we pass the current display to show the bezier line that could have been there.
                    takePic(display,savePath)





# FD. updateButtons()
# purp. change the colors of the buttons, and handle switches controlling the program's modes
def updateButtons():
    global measureMode
    global isPressingScreenButton
    global scalebarMode
    global scalebar
    global line
    global savePath
    for button in lob:
        # if the cursor hovers the button, change its color
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            # evaluate if user wants to click on a button
            if isPressingScreenButton:
                button.color = (100,100,100)
                if button.name == "SCALEBAR":
                    measureMode = True
                    scalebarMode = True 
                    scalebar = Scalebar()
                    # scalebar.resetTimer()
                elif button.name == "LINE":
                    measureMode = True
                    scalebarMode = False #line mode is a free parameter given when scalebarMode is False
                    line = Line()
                elif button.name == "SET PATH..":
                    savePath = save_as_dialog()
                elif button.name == "PICTURE":
                    updateDisplay_forImageTaking()
                    takePic(display,savePath)
            else:
                button.color = (200,200,200)
        else:
            button.color = button.original_color


    
def update():
    global measureMode
    updateUserInput()   # Listen to user input
    if not measureMode: updateButtons()     # update button colors and program modes
    # elif scalebarMode: updateScalebar()
    # else: updateLine()
    
        
        

    
    
while True:
    draw()
    update()