# IMPORTS
import pygame 
import os 
import math 
# DD
SCREEN = (1200,800)
display = pygame.display.set_mode(SCREEN)

# DD. SUBDIVISIONS
# subdivs = int
# interp. the number of subdivisions for each segment in the Bezier curve
SUBDIVS = 100
SEGMENT_DISTANCE = 1/SUBDIVS #how long is a segment relative to a unit

# DD. BEZIER
# bezier = Bezier()
# interp. an object representing a Bezier unit that contains:
# - point 1
# - point 2 (anchor)
# - point 3
# DD. BEZIER_UNIT
# bu = Bu()
# interp. all the elements involved in calculating a bezier curve
class Bu():
    def __init__(self,pA=(0,0),pG=(0,0),pB=(0,0),color="green"):
        self.pA = pA
        self.pG = pA
        self.pG_inverse = self.pG
        self.pB = self.pA #set the starting and end position of the line at the same point at the beginning
        self.color = color
        # self.isActive = True #determines whether the points G and B that make the unit should change
        self.ptA_Set = True
        self.ptB_Set = False #determines whether the points G and B that make the unit should change
        self.finishedBu = False
        self.draw_laterals = False #activates when the lateral lines reflecting gravity points have to show up
        self.saved_points = [] 
    
    def draw(self):
        # if self.ptA_Set and not self.ptB_Set:
        #     self.pB = self.pG = pygame.mouse.get_pos()
            
        # RENDER THE LINE SEGMENTS OF THE BEZIER CURVE
        startingX = self.pA[0]
        startingY = self.pA[1]
        for i in range(SUBDIVS):
            # Calculate the relative distance traveled in the time i starting at A
            x1 = self.pA[0] + (self.pG[0] - self.pA[0]) * (i * SEGMENT_DISTANCE)
            y1 = self.pA[1] + (self.pG[1] - self.pA[1]) * (i * SEGMENT_DISTANCE)

            x2 = self.pG[0] + (self.pB[0] - self.pG[0]) * (i * SEGMENT_DISTANCE)
            y2 = self.pG[1] + (self.pB[1] - self.pG[1]) * (i * SEGMENT_DISTANCE)

            x = x1 + (x2 - x1) * (i * SEGMENT_DISTANCE)
            y = y1 + (y2 - y1) * (i * SEGMENT_DISTANCE)

            pygame.draw.line(display,self.color,(startingX,startingY),(x,y),3)

            startingX = x
            startingY = y

        # draw auxiliary lines to reshape the Bezier curve
        if self.draw_laterals:
            # get the angle between the point B and the position of the cursor
            mx, my = pygame.mouse.get_pos()
            a = mx - self.pB[0]
            o = my - self.pB[1]
            angle = math.atan2(o,a)
            radius = (a**2 + o**2)**0.5
            x_G_inverse = self.pB[0] + (math.cos(angle) * radius)
            y_G_inverse = self.pB[1] + (math.sin(angle) * radius)
            x_G = self.pB[0] - (math.cos(angle) * radius)
            y_G = self.pB[1] - (math.sin(angle) * radius)
            self.pG = x_G,y_G
            self.pG_inverse = x_G_inverse,y_G_inverse
            pygame.draw.line(display,self.color,self.pB, self.pG,2)
            pygame.draw.line(display,self.color,self.pB, self.pG_inverse,2)
            pygame.draw.circle(display,self.color,self.pG,4)
            pygame.draw.circle(display,self.color,self.pG_inverse,4)
    
    def savePoints(self):
        startingX = self.pA[0]
        startingY = self.pA[1]
        for i in range(SUBDIVS):
            # Calculate the relative distance traveled in the time i starting at A
            x1 = self.pA[0] + (self.pG[0] - self.pA[0]) * (i * SEGMENT_DISTANCE)
            y1 = self.pA[1] + (self.pG[1] - self.pA[1]) * (i * SEGMENT_DISTANCE)

            x2 = self.pG[0] + (self.pB[0] - self.pG[0]) * (i * SEGMENT_DISTANCE)
            y2 = self.pG[1] + (self.pB[1] - self.pG[1]) * (i * SEGMENT_DISTANCE)

            x = x1 + (x2 - x1) * (i * SEGMENT_DISTANCE)
            y = y1 + (y2 - y1) * (i * SEGMENT_DISTANCE)

            pygame.draw.line(display,self.color,(startingX,startingY),(x,y),3)

            startingX = x
            startingY = y
            self.saved_points.append((startingX,startingY))
            
    # Go over points that make the Bezier to get total scaled distance, by knowing the units per pixel scale
    def calculateDistance(self, unitsPerPixel):
        total = 0
        for i_pt,pt in enumerate(self.saved_points-1):
            # calculate distance between i_pt and i_pt + 1
            a_ = self.saved_points[i_pt+1][0] - pt[0]
            o_ = self.saved_points[i_pt+1][1] - pt[1]
            total += (a_**2 + o_**2) ** 0.5
        return total
            
bu0 = Bu((100,100),(150,200),(300,350))
bu1 = Bu((100,200),(300,260),(350,100))

# DD. SPLINE
# spline = Spline()
# interp. the collection of Bezier units that create a spline
class Spline():
    def __init__(self):
        self.first_click = False
        self.lobu = []
    
    def draw(self):
        for bu in self.lobu:
            bu.draw()
        
    def onMouseEventUp(self):
        if self.first_click:
            self.first_click = False 
        else:
            if len(self.lobu)>0:
                last_bu = self.lobu[-1] #THE LAST ELEMENT IS THE PREVIOUS BEZIER UNIT, that has already been finished
                # if the previous Bu is finished, create the next one
                if last_bu.finishedBu:                    
                    bu = Bu(last_bu.pB)
                    # if there's already other Bu's, use the previous (i = -1) Bu
                    # variable lastbu.pG for this pG pos
                    bu.pG = last_bu.pG_inverse
                    self.lobu.append(bu)
                elif last_bu.ptA_Set and last_bu.ptB_Set:
                    last_bu.finishedBu = True 
            else:
                bu = Bu(pygame.mouse.get_pos())
                self.lobu.append(bu)
                
    def onMouseEventDown(self):
        # if last Bu in lobu exists, has ptA set, ptB not set and is not finishedBu
        # mark point B as done
        if len(self.lobu)>0:
            last_bu = self.lobu[-1] #active bezier unit is last in the list
            if last_bu.ptA_Set and not last_bu.ptB_Set and not last_bu.finishedBu:
                print("mouse down successfully sets ptB_Set to True")
                last_bu.ptB_Set = True
            
    
    def update(self):
        if len(self.lobu)>0:
            last_bu = self.lobu[-1] #the active bezier unit
            if last_bu.ptA_Set and not last_bu.ptB_Set and not last_bu.finishedBu:
                last_bu.pB = pygame.mouse.get_pos()
            elif last_bu.ptA_Set and last_bu.ptB_Set and not last_bu.finishedBu:
                # !!! Draw gravity lines using pointer and draw Bezier curves
                last_bu.draw_laterals = True
                # last_bu.pB = pygame.mouse.get_pos()
            elif last_bu.ptA_Set and last_bu.ptB_Set and last_bu.finishedBu:
                last_bu.draw_laterals = False
                last_bu.savePoints() #store the positions of each point that makes the spline to help calculations later on
            
    # calculate the total distance of the Bezier spline
    def calculateTotalWeights(self,unitsPerPixel):
        total_length = 0
        for bu in self.lobu:
            total_length += bu.calculateDistance(unitsPerPixel)
            
        
        
        
spline = Spline()
# spline.AddBu((100,100))
# CODE

def draw():
    display.fill("black")
    spline.draw()
    pygame.display.flip()
    
def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                spline.onMouseEventUp()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spline.onMouseEventDown()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                spline.calculateTotalWeights(0.1)
        spline.update()

while True: draw(); update()