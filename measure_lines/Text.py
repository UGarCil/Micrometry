import pygame
from constants import *


# DD. TEXT
# text = Text()
# interp. a piece of text to provide information into the program via buttons or warnings
class Text():
    def __init__(self, content,x,y,size,color="black"):
        self.content = content
        self.color = color
        self.x = x 
        self.y = y 
        self.size = size
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        
        # create a text surface object,
        # on which text is drawn on it.
        self.text = self.font.render(self.content, True, self.color)
        
        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        
        
    def draw_text(self):
        # set the center of the rectangular object.
        self.textRect.center = (self.x, self.y)
        display.blit(self.text, self.textRect)
        


# DD. TEXT_ALARM
# text = Text()
# interp. a piece of text to provide information into the program via buttons or warnings
class TextAlarm():
    def __init__(self, content,x,y,size,timer=1200):
        self.content = content
        self.timer = timer
        self.x = x 
        self.y = y 
        self.size = size
        self.start_time = pygame.time.get_ticks()
        self.isRunningTimer = True #once the number of ticks gets over the threshold, stop reading the frames to enhance memory
        
        # 2nd parameter is size of the font
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        
        # create a text surface object,
        # on which text is drawn on it.
        self.text = self.font.render(self.content, True, "red")
        
        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        # set the center of the rectangular object.
        self.textRect.center = (self.x, self.y)
        
    def draw_text(self):
        if self.isRunningTimer:
            if pygame.time.get_ticks() - self.start_time <= self.timer:
                display.blit(self.text, self.textRect)
            else:
                self.isRunningTimer = False
        
        