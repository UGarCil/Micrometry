import pygame
from Text import Text
from constants import *


# DD. BUTTON
# button = Button()
# interp. a rectangular object with text inside that triggers an event
class Button():
    def __init__(self,x,y, w,h,name, text_size = 16,timer=150,text_color = "black"):
        self.text_size = text_size
        self.x =x
        self.y =y 
        self.w = w 
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.rect.topleft = self.x, self.y
        self.original_color = "white"
        self.color = self.original_color
        self.name = name
        self.text_color = text_color
        self.text = Text(self.name,self.x + self.w//2, self.y + self.h//2,self.text_size, color=text_color)
        self.timer = timer #sets the number of frames in between button listening events
        self.start_time = pygame.time.get_ticks() #track the last time the button was clicked
        self.ready = True
        
    
    def draw(self):
        self.updateRect()
        self.updateRecoil()
        pygame.draw.rect(display,self.color, self.rect)
        self.text.draw_text()
        
    def updateRect(self):
        self.rect.topleft = self.x, self.y
        self.text.textRect.center = self.x + self.w//2, self.y + self.h //2
    
    def updateName(self):
        self.text = Text(self.name,self.x + self.w//2, self.y + self.h//2,self.text_size,self.text_color)
    
    def updateRecoil(self):
        # there is a very small chance the user will click when the tick control system wraps around
        delta_ticks = pygame.time.get_ticks() - self.start_time
        if delta_ticks <0: 
            self.start_time =0
        # if delta is bigger than the timer, it means we're ready to press the button again
        if not self.ready and delta_ticks >= self.timer:
            self.ready = True
    
    def resetRecoil(self):
        self.ready = False 
        self.start_time = pygame.time.get_ticks()