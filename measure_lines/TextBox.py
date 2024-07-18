import pygame
from constants import *

# DD. TEXT_BOX
# textBox = Textbox()
# interp. a rectangular box that accepts the user's input as numbers and dot
class Textbox():
    def __init__(self,x,y,color,size=16,prefix="len "):
        self.x = x 
        self.y = y 
        self.color = color 
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.prefix = prefix #tag that will inform user what to type
        self.input_text = ""
        self.isACTIVE = True
        self.value = -1

        
        # create a text surface object,
        # on which text is drawn on it.
        # self.text = self.font.render(self.input_text, True, self.color)
        
        # create a rectangular object for the
        # text surface object
        # self.textRect = self.text.get_rect()
        # set the center of the rectangular object.
        # self.textRect.center = (self.x, self.y)
    
    def draw(self):
        if self.isACTIVE:
            text_surface = self.font.render(self.prefix + self.input_text, True, self.color)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            display.blit(text_surface, text_rect)





