from constants import *
from Text import Text

# DD. SCALEBAR
# scalebar = Scalebar()
# interp. create a line between two points representing the scalebar
class Scalebar():
    def __init__(self):
        self.isPt1Done = False 
        self.isPt2Done = False 
        self.pt1 = (-100,-100)
        self.pt2 = (-100,-100)
        self.firstClick = True
        self.valuePixels = -1   #distance values of 0 are possible, but not -1, making value good default
        self.valueUnits = -1    #measurement values of 0 are possible, but not -1, making value good default
        self.ratioPixelUnits = -1
        # self.follow_the_mouse = False 
        
    def draw(self):
        if self.isPt1Done and not self.isPt2Done:  
            pygame.draw.line(display,"red",self.pt1,pygame.mouse.get_pos(),2)
        elif self.isPt1Done and self.isPt2Done:
            pygame.draw.line(display,"red",self.pt1,self.pt2,2)
            
    
    def calibrateScalebar(self,distance):
        a = self.pt2[0] - self.pt1[0] 
        o = self.pt2[1] - self.pt1[1] 
        h = (a**2 + o**2)**0.5 #distance between the two points in pixels
        self.valueUnits = distance 
        self.valuePixels = h
        # (units/pixels) provides how many units are in 1 pixel
        self.ratioPixelUnits = self.valueUnits/self.valuePixels
    

# DD. LINE
# line = Line()
# interp. a line projected from two points to make a measurement
class Line():
    def __init__(self):
        self.isPt1Done = False 
        self.isPt2Done = False 
        self.pt1 = (-100,-100)
        self.pt2 = (-100,-100)
        self.firstClick = True
        self.value = "N/A"
        self.text = Text(str(self.value),0,0,16,"green")
        # self.follow_the_mouse = False 
        
    def draw(self,scalebar):
        mousePos = pygame.mouse.get_pos()
        if self.isPt1Done and not self.isPt2Done:  
            pygame.draw.line(display,"green",self.pt1,mousePos,2)
            self.pt2 = mousePos[0], mousePos[1]
        elif self.isPt1Done and self.isPt2Done:
            pygame.draw.line(display,"green",self.pt1,self.pt2,2)
        self.text.x,self.text.y = self.pt2[0]-16,self.pt2[1]-16
        self.interpolateWithScalebar(scalebar)
        self.text.draw_text()

    def interpolateWithScalebar(self,scalebar):
        # create an interpolation with the value of the scalebar
        # if the scalebar has been set, calculate the ratio
        if scalebar.ratioPixelUnits >=0:
            a = self.pt2[0] - self.pt1[0]
            o = self.pt2[1] - self.pt1[1]
            h = (a**2 + o**2)**0.5
            self.value = scalebar.ratioPixelUnits * h
            # update the value of the 
            self.text.content = str(round(self.value,3))
            self.text.text = self.text.font.render(self.text.content, True, self.text.color)