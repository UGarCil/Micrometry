# Apply the Mixture of Gaussians algorithm to generate a mask against the background to improve line contrast

from constants import *


objectDetector = cv2.createBackgroundSubtractorMOG2()


def mog3(frame):
    # Apply the Background substractor based on a frame. In this case the initial frame
    mask = objectDetector.apply(frame)
    # # Find the contours in the mask to filter over a threshold
    # contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     if area > 100:
    #         cv2.drawContours(frame,[cnt],-1,(0,255,0))

    # cv2.imshow("Frame2",frame)
    return mask