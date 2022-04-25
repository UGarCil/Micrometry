# MODULES
import math
from matplotlib.pyplot import text
import pygame
import cv2
from PIL import Image
import numpy as np




# DATA DEFINITIONS


# CONSTANTS
SCREEN = (1000,1000*.74)

# Variables required by pygame
display = pygame.display.set_mode(SCREEN)
clock = pygame.time.Clock()
pygame.init()


# Data def. MOUSE_X
# xm = int
# interp. the x position of the mouse on the screen
xm0 = 0
xm1 = 10
xm2 = 100

# Data def. MOUSE_Y
# ym = int
# interp. the y position of the mouse on the screen
ym0 = 0
ym1 = 10
ym2 = 100

# Data def. CAPTURE
# cap = cv2.VideCapture(int)
# interp. cv2 object capturing the images from a webcam. 0 is default for integrated computer webcam
cap0 = cv2.VideoCapture(0)

# Data def. BUTON_X
# btX = int
# interp. the position of the button relative to the screen in X
btX0 = 20

# Data def. BUTON_Y
# btY = int
# interp. the position of the button relative to the screen in Y
btY0 = 20


class Main():

    def __init__(self, width, height, cap):
        self.xm = 0
        self.ym = 0
        self.MouseDown = False #if False
        self.resetAnchorMousePos = True #if True, will anchor pos on first click
        self.FirstPOS = (0,0)
        self.SecondPOS = (0,0)
        self.widthCAP = width
        self.heightCAP = height
        self.cap = cap
        self.frame = None
        self.text = None
        self.textRect = None

        # Button properties
        # self.btX = btX0
        # self.btY = btY0
        # self.btWidth = 128
        # self.btHeight = 32
        # self.buttonColor = (30,30,30)
        # self.buttonFontColor = (255,255,255)
        # self.buttonFont = pygame.font.Font('freesansbold.ttf', 16)
        # self.BT_TEXT = self.buttonFont.render("SET SCALEBAR", True, self.buttonFontColor)
        # self.buttonPressed = False
        # self.BT_TEXTRECT = self.BT_TEXT.get_rect(center=(self.btWidth/2, self.btHeight/2))
        self.SPR_BT_OFF = pygame.image.load("./Images/Button_small.png")
        self.SPR_BT_ON = pygame.image.load("./Images/Button_small_ON.png")
        self.SPR_XPOS = 10
        self.SPR_YPOS = 10
        self.BT_WIDTH = self.SPR_BT_OFF.get_width()
        self.BT_HEIGHT = self.SPR_BT_OFF.get_height()
        self.ButtonPressed = "Inactive"  #Button has three states: Inactive, Mesuring, Finished
        # self.resetBtnActiveTimer = 10
        # self.BtnActiveTimer = self.resetBtnActiveTimer


        # Scalebar
        self.magnitud = "mm"
        self.distanceUnits = 0


    def Manager(self):
        while True:
            self.getFrame()
            self.getUserCommands()
            self.render()

    def getFrame(self):
        ret0, frame0= self.cap.read()
        imS0 = cv2.resize(frame0, (self.widthCAP,self.heightCAP))
        self.frame= np.rot90(frame0)
        self.frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        self.frame=pygame.surfarray.make_surface(self.frame)

    def executeButton(self):
        pass


    def getUserCommands(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap0.release()
                cv2.destroyAllWindows()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.MouseDown = True
                    # Get area range occupied by button
                    inXRange = pygame.mouse.get_pos()[0] >= self.SPR_XPOS and pygame.mouse.get_pos()[0] <= self.SPR_XPOS + self.BT_WIDTH
                    inYRange = pygame.mouse.get_pos()[1] >= self.SPR_YPOS and pygame.mouse.get_pos()[1] <= self.SPR_YPOS + self.BT_HEIGHT
                    # If user clicks button, change from whatever the state is to "Waiting"
                    if inXRange and inYRange:
                        self.ButtonPressed = "Waiting"
                    else:
                        # Get current mouse pos when first clicked
                        if self.resetAnchorMousePos:
                            self.FirstPOS = pygame.mouse.get_pos()
                            self.resetAnchorMousePos = False     #Don't reset the mouse's first pos just yet! Wait until button up!
            
            if self.MouseDown:
                self.SecondPOS = pygame.mouse.get_pos() #Get second mouse position
                if self.ButtonPressed == "Inactive":
                    self.printMeasurementScreen()


            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.MouseDown = False
                    if self.ButtonPressed == "Measuring":
                        self.ButtonPressed = "Inactive"
                        self.distanceUnits = self.pitagoras()
                    if self.ButtonPressed == "Waiting":
                        self.ButtonPressed = "Measuring"

                    self.resetAnchorMousePos = True

    def pitagoras(self):
            dX = self.FirstPOS[0] - self.SecondPOS[0]
            dY = self.FirstPOS[1] - self.SecondPOS[1]
            pit = math.sqrt(dX**2 + dY**2)
            return(pit)

    def printMeasurementScreen(self):
        font = pygame.font.Font('freesansbold.ttf', 24) # create a font object.
        
        try:
            self.text = font.render(f"{(self.pitagoras()/self.distanceUnits):.2f}", True, (0,255,0), (0,0,255)) # create a text surface object,
        except:
            self.text = font.render(f"{0.00:.2f}", True, (0,255,0), (0,0,255))
        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        
        # set the center of the rectangular object.
        self.textRect.center = (self.FirstPOS[0], self.FirstPOS[1])


    def render(self):
        display.fill((30,30,30))
        display.blit(self.frame, (0,0))

        # Measuring Mode
        if self.MouseDown and self.ButtonPressed == "Inactive":
            pygame.draw.line(display, (255, 0, 0), (self.FirstPOS[0], self.FirstPOS[1]), (self.SecondPOS[0], self.SecondPOS[1]))
            display.blit(self.text, self.textRect)

        # Calibration Mode
        elif self.MouseDown and self.ButtonPressed == "Measuring":
            pygame.draw.line(display, (0, 255, 0), (self.FirstPOS[0], self.FirstPOS[1]), (self.SecondPOS[0], self.SecondPOS[1]))
            # display.blit(self.text, self.textRect)

        # Draw the button
        if self.ButtonPressed == "Measuring" or self.ButtonPressed == "Waiting":
            display.blit(self.SPR_BT_ON, (self.SPR_XPOS, self.SPR_YPOS))
        else:
            display.blit(self.SPR_BT_OFF, (self.SPR_XPOS, self.SPR_YPOS))
        

        pygame.display.flip()
    

instance = Main(1000,int(1000*.74), cap0)
while True:
    instance.Manager()
    



