from constants import *

# DD. BOX
# box = Box()
# interp. a square that will delimit the area that will be sampled to create an input to a dataset
class Box():
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.w = 0
        self.h = 0
        self.color = "green"
        self.firstClick = True
        self.firstMouseEvent = False 
        self.secondMouserEvent = False
        # temporary values for subquadrant calculations
        self.tempX = self.x 
        self.tempY = self.y
        self.quadrant = None
        self.updateConditions()
        self.updateRect()
        self.waitingForPrefix = False
        
    def draw(self):
        self.updateRect()
        # the lines of the box show up when handling the box as a numpy array. Condition helps deactivating the lines before processing
        if not self.waitingForPrefix:
            pygame.draw.rect(display,self.color,(self.tempX, self.tempY,self.w, self.h),2)
    
    def getQuadrant(self,mx,my):
        # 2 | 3 
        # --|--
        # 1 | 0
        if mx - self.x >=0:
            if my - self.y >=0:
                # case 0: right bottom SubQuad
                return 0
            else:
                # case 3: right top SubQuad
                return 3
        else:
            if my - self.y >=0:
                # case 1: left bottom SubQuad
                return 1
            else:
                # case 2: left top SubQuad
                return 2
            
    
    def updateRect(self):
        # stage2 is dragging mode
        if self.stage2:
            mx,my = pygame.mouse.get_pos()
            # get the subquadrant, in cartesian plane, where the mousePos is relative to fixed point x,y
            self.quadrant = self.getQuadrant(mx,my)
            # if quadrant != self.lastquadrant:
            #     self.w = 0
            #     self.h = 0
            #     self.lastquadrant = quadrant
                
            if self.quadrant == 0:
                self.tempX = self.x
                self.tempY = self.y
                self.w = mx - self.x
                # self.h = self.w
                self.h = my-self.tempY
            elif self.quadrant == 1:
                self.tempX = mx
                self.w = self.x - self.tempX
                self.tempY = self.y
                # self.h = self.w
                self.h = my-self.tempY
            elif self.quadrant == 2:
                self.tempX = mx
                self.w = self.x - mx
                # self.tempY = self.y - self.w
                self.tempY = my
                # self.h = self.w
                self.h = self.y - self.tempY
            else:
                self.tempX = self.x
                self.w = mx - self.x
                # self.tempY = self.y - self.w
                self.tempY = my
                # self.h = self.w
                self.h = self.y - self.tempY
            
            
        # self.rect = pygame.Rect(self.x, self.y,self.w, self.h)
        # self.rect.topleft = self.x, self.y
    
    def updateConditions(self):
        # STAGES:
        # 1. user's first box selection click down
        self.stage1 = not self.firstMouseEvent and not self.secondMouserEvent 
        # 2. user's dragging selection 
        self.stage2 = self.firstMouseEvent and not self.secondMouserEvent
        # 3. user's confirmed second click
        self.stage3 = self.firstMouseEvent and self.secondMouserEvent
    
    def onMouseDown(self):
        if self.stage1:
            self.x, self.y = pygame.mouse.get_pos()
            self.firstMouseEvent = True
            self.tempX = self.x 
            self.tempY = self.y
        elif self.stage2:
            self.secondMouserEvent = True
        self.updateConditions()
    
    # Depending on the quadrant, reposition the coordinates x and y to be the top left corner of the box
    def updatePointOfOrigin(self):
        self.x = self.tempX
        self.y = self.tempY
            
    
    