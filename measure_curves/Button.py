import pygame
from Text import Text
from constants import *


# DD. BUTTON
# button = Button()
# interp. a rectangular object with text inside that triggers an event
class Button():
    def __init__(self,x,y, w,h,name, text_size = 16):
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
        self.text = Text(self.name,self.x + self.w//2, self.y + self.h//2,self.text_size)
    
    def draw(self):
        self.updateRect()
        pygame.draw.rect(display,self.color, self.rect)
        self.text.draw_text()
        
    def updateRect(self):
        self.rect.topleft = self.x, self.y
        self.text.textRect.center = self.x + self.w//2, self.y + self.h //2