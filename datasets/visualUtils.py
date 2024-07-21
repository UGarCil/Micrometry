# # MODULES
import os
import numpy as np
import pygame

# # Initialize pygame
# pygame.init()

# Screen dimensions



# Load your image data (assuming Monas.npy contains valid image data)
img = np.load("testIMG.npy")
len_img = img.shape
RES = 2
WIDTH = len_img[0] * RES
HEIGHT = len_img[1] * RES
# Create a window
display = pygame.display.set_mode((WIDTH, HEIGHT))
squareImg = img[0]  # Assuming img[0] is a 28x28 image

# DD. PIXEL
# pix = Pixel()
# interp. a square somewhere in the SCREEN


class Pixel():

  def __init__(self, c, r, colour):
    self.c = c
    self.r = r
    self.x = self.c * RES
    self.y = self.r * RES
    self.colour = colour
    self.rect = pygame.Rect(self.x, self.y, RES, RES)

  def draw(self):
    pygame.draw.rect(display, self.colour, self.rect)


# DD. GRID
# grid = [[PIXEL, ..., n=28], ..., n=28]
# interp. a 3D grid of PIXEL
grid = []
for r in range(len_img[0]):
  row = []
  for c in range(len_img[1]):
    pix = Pixel(c, r, img[r][c])
    row.append(pix)
  grid.append(row)

# TEMPLATE FOR GRID
#  for row in grid:
#     for pix in row:
#       ... pix


def updateGrid(i):
  squareImg = img[i].reshape(28, 28)  # Assuming img[0] is a 28x28 image
  for r, row in enumerate(grid):
    for c, pix in enumerate(row):
      color = squareImg[r][c]
      pix.colour = (color, color, color)


i = 0

################### CODE ###################


def draw():
  # Draw the square
  for row in grid:
    for pix in row:
      pix.draw()
  # Update display
  pygame.display.flip()


def update():
    global running
#   global i
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#   i = (i + 1)%len_img

#   updateGrid(i)


running = True
while running:
  draw()
  update()

pygame.quit()

# https://www.youtube.com/watch?v=FzG4uDgje3M&list=PLo1G34n886O-Yz4O-uSpORqsiuJ4xMJlb&index=2
