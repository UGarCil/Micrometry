from constants import *


objectDetector = cv2.createBackgroundSubtractorMOG2()


def mog3(frame):
    mask = objectDetector.apply(frame)
    return mask

# FD. updateCV2Frames()
# purp. create a surface class object with the feed from the webcam
def updateCV2Frames(freeze_on=False):
    global frame,surface
    # global first,idx
    _,frame = cap.read()
    if not freeze_on:
        surface = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = cv2.rotate(surface, cv2.ROTATE_90_COUNTERCLOCKWISE)
        surface = cv2.flip(surface,0)
        surface = cv2.resize(surface, (H,W))  #HEIGHT AND WIDTH get flipped because or the counterclockwise rotation
        if edgeMode:
            surface = mog3(surface)
        surface = pygame.surfarray.make_surface(surface)
    display.blit(surface,(0,0))
    return surface