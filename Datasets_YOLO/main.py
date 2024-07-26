# This program is an extension of the suite of utilities for Micrometry found at github.com/ugarCil/Micrometry, and 
# allows the user for gathering images in a way similar to the software labelImg: it freezes an image to allow the user
# to delimit bounding boxes. The image gets saved in the folder images, and the labels get saved in a txt file that contains 
# the parameters of all the boxes that were delimited for that image, in the YOLO format:
#   class   center_positionX    center_positionY    width   height
# All values, other than class, are normalized, in such a way that the top left corner of the screen is position 0,0
# and the bottom right corner is position 1,1

# IMPORT
from constants import *
from Button import Button
from cv2Utils import updateCV2Frames
from Box import Box
from Text import TextAlarm
from PictureManager import saveImage


# DD. BUTTON
# button = Button()
# interp. a button to be displayed in the screen
button  = Button(W//32,H//32,W//10,H/24,"ANNOTATE",text_size=14)

# LIST_OF_BUTTONS
# lob = [BUTTON, ...]
# interp. the collection of buttons that make the GUI
lob = [button]


# DD. BOX
# box = Box()
# interp. a bounding box that allows the user to subsample an image from the display view
# box = Box()

# DD. ACTIVE_BOX
# activeBox = BOX instance
# interp. the box whose text is currently being edited
activeBox = None

# DD. LIST_OF_BOX
# lobox = [BOX, ...]
# interp. a collection of boxes to save along with the frozen image
lobox = []

# DD. TEXT_ALARM
# text_alarm = TEXT_BOX
# interp. a block of text that appears in the screen for some time to alert user of potential issues
text_alarm = TextAlarm("",-100,-100,0)

# DD. SURFACE
# surface = pygame.Surface()
# interp. a 2D array of pixels saved as a pygame object, useful to save an image of reference coming from the program
surface = None

# CODE

# Set booleans to the initial state of the program
def resetBooleans():
    global freeze_on
    global edgeMode
    global isMouseDown
    global isEditMode
    global lobox
    # global WaitingForBoxLabel
    global activeBox
    freeze_on = False 
    edgeMode = False
    isMouseDown = False
    isEditMode = False
    # WaitingForBoxLabel = False
    activeBox = None
    lobox = []

def draw():
    global surface
    surface = updateCV2Frames(freeze_on)
    [button.draw() for button in lob]
    [box.draw() for box in lobox]
    text_alarm.draw_text()
    pygame.display.flip()

def makeNewBox():
    box = Box(mousePos[0],mousePos[1])
    lobox.append(box)
    

# FD. saveLabels()
# purp. store the label information in a txt file with the name of the image they came from
def saveLabels(fileName):
    fileName = os.path.split(fileName)[1].replace(ife,"")
    # if the folder labels doesn't exists, make it
    os.mkdir("labels") if not os.path.exists("./labels/") else None
    with open(f"./labels/{fileName}.txt","w") as file:
        textContent = ""
        for box in lobox:
            # find the index of the box's label in classes
            if box.label in classes:
                textContent += str(classes.index(box.label))
            # normalize the box's positions in x and y
            textContent += "\t"+str(round((box.x + box.w//2)/W,6))
            textContent += "\t"+str(round((box.y + box.h//2)/H,6))
            # normalize the box's width and height
            textContent += "\t"+ str(round(box.w/W,6))
            textContent += "\t"+ str(round(box.h/H,6))
            textContent += "\n"
        file.write(textContent)
    # save the classes list as a .txt as well
    with open("./labels/classes.txt","w") as class_file:
        class_file.write("\n".join(classes))
        
            
def isMouseDown_UserInput(event):
    global isMouseDown
    # evaluate interaction with buttons
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not isEditMode:
        isMouseDown = True
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not isEditMode:
        isMouseDown = False

def isMouseDownRight_UserInput(event):
    global isMouseDownRight
    
    def eraseOverlappingBoxes():
        for box in lobox:
            if box.SelectedForDelete and not box.WaitingForBoxLabel:
                lobox.remove(box)
    
    # evaluate whether the right button mouse is being held down
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and isEditMode:
        print(mousePos)
        isMouseDownRight = True

    # evaluate whether the right button mouse is NOT being held down
    if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and isEditMode:
        isMouseDownRight = False
        eraseOverlappingBoxes()

def reset_UserInput(event):
    # reset option when pressing ESCAPE
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        resetBooleans()
        activateButtons()

def lobox_UserInput():
    global activeBox
    # if last box in the list lobox is still active, update it
    if len(lobox) >0 and lobox[-1].isACTIVE:
        lobox[-1].onMouseDown()
        if not lobox[-1].isACTIVE:
            # Set the state of the program to waiting for label from user, ignoring other inputs
            activeBox = lobox[-1]
            activeBox.WaitingForBoxLabel = True
            # create a new textBox to receive the user's input
    # else create a new box
    else:
        # if there is no active box or the current active box has been completed by adding it label
        if activeBox == None or not activeBox.WaitingForBoxLabel:
            makeNewBox()

def editLabel_UserInput(event):
    global text_alarm
    # if last box in the list lobox is still active, update it
    # The tag given to a measurement can include any letter, number and some special characters
    if event.unicode.isalnum() or event.unicode in validLineNames:
        activeBox.label += event.unicode
    # Handle backspace to delete characters
    elif event.key == pygame.K_BACKSPACE:
        activeBox.label = activeBox.label[:-1]
    # Handle return/enter to finish input
    elif event.key == pygame.K_RETURN:
        if len(activeBox.label) <1:
            # if not os.path.exists(savePath):
            text_alarm = TextAlarm("Please enter at least one character",W//2,H-80,16,2000)
        # stop editing the label and turn waitingForBoxLabel off
        else:
            activeBox.WaitingForBoxLabel = False
            activeBox.updatePointOfOrigin() #Make sure the top left corner of the box is its coordinates x and y
            activeBox.toggleLabelText.content = activeBox.label

def processBox():
    # SavePicture
    fileName = saveImage(surface)
    # Update the labels 
    for box in lobox:
        if box.label not in classes:
            classes.append(box.label)
    # Save the labels into a txt file
    saveLabels(fileName)
    resetBooleans()
    activateButtons()

def shortcuts_UserInput():
    global freeze_on
    global isEditMode
    # if there are no delimited boxes, allow the user to enter freeze mode with space bar back and forth
    if len(lobox) ==0:
        if isEditMode:
            print("activate Buttons")
            activateButtons()
            freeze_on = False 
            isEditMode = False
        else:
            print("deactivate buttons")
            deactivateButtons()
            freeze_on = True
            isEditMode = True


def userInputManager():
    global isMouseDown
    global text_alarm
    global freeze_on
    global isEditMode
    global isMouseDownRight
    # global WaitingForBoxLabel
    global activeBox
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        
        # evaluate is user is pressing the left mouse button
        isMouseDown_UserInput(event)
        # evaluate if user is holding down right mouse button
        isMouseDownRight_UserInput(event)
        
        # evaluate if the user pressed ESCAPE to cancel edit mode and reset the system
        reset_UserInput(event)
        
        # evaluate if user wants to use shortcuts while not on edit mode
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shortcuts_UserInput()
        
        # evaluate interaction with boxes in edit mode when left mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and isEditMode:
            lobox_UserInput()
        
        # evaluate interaction with boxes in edit mode when right mouse button down
        if isMouseDownRight and isEditMode:
            if len(lobox)>0:
                for box in lobox:
                    # mouse position is globally updated via function updateButtons()
                    if box.rect.collidepoint(mousePos):
                        box.SelectedForDelete = True
                    else:
                        box.SelectedForDelete = False
        
        
        # Once there's an active box that is ready to have its label edited (stage 3), handle user's input for the last active box
        # INVARIANT: len(lobox) > 0
        if event.type == pygame.KEYDOWN and isEditMode and activeBox != None and activeBox.WaitingForBoxLabel:
            editLabel_UserInput(event)
            
        # evaluate user input for ending edit mode and saving the images and their labels
        if event.type == pygame.KEYDOWN and isEditMode and activeBox != None and not activeBox.WaitingForBoxLabel and event.key == pygame.K_d:
            processBox()
                    
        
        
                    
                    
            
            
def deactivateButtons():
    # deactivate all buttons
    for button in lob:
        button.isACTIVE = False
def activateButtons():
    # deactivate all buttons
    for button in lob:
        button.isACTIVE = True
        button.color = button.original_color


def updateButtons():
    global mousePos
    global freeze_on
    global isEditMode
    # update Mouse position
    mousePos = pygame.mouse.get_pos()
    
    # lower color opacity for interactive effect if user hovering buttons OR..
    if not isMouseDown:
        for button in lob:
            button.highlight(mousePos)
    # Evaluate button pressing
    else:
        for button in lob:
            buttonName = button.press(mousePos)
            if buttonName == "ANNOTATE":
                deactivateButtons()
                freeze_on = True
                isEditMode = True
            # OTHER BUTTONS HERE
    

def update():
    userInputManager()
    updateButtons()
    
while True: draw();update()