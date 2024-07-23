from constants import *
import numpy as np
from padding import get_padded_image

def contains_numeric(s):
    num = ""
    if any(char.isdigit() for char in s):
        for char in s:
            if char.isdigit():
                num += char
        return int(num)
    return 0

    # Navigate the dir images and determine the next item in the sequence
def getFileName(path,prefix):
    # get a list of the items in the dir
    files = os.listdir(path)
    files = [x.split(".")[0] for x in files]
    files = [x.split("_")[1] for x in files]
    files = [contains_numeric(x) for x in files]
    if len(files)>0:
        maxFileNum = max(files)
        nextDigit = maxFileNum+1
    else:
        nextDigit = 0
    totalDigits = len(str(nextDigit))
    finalName = ["0" for _ in range(6-totalDigits)]
    finalName = prefix + "_" + "".join(finalName)+ str(nextDigit) + ".png"
    finalName = jn(path,finalName)
    # print(finalName)
    # print(os.path.exists(finalName))
    return (finalName)





# FD. saveImage()
# purp. process the coordinates delimited by a box into an image with a given prefix
def saveImage(box,prefix):
    # determine if the folder images has been created
    os.mkdir("images") if not os.path.exists("./images/") else None
    # determine if the folder with the prefix name has been created, if not make it
    os.mkdir(f"./images/{prefix}") if not os.path.exists(f"./images/{prefix}") else None
    
    # Get the file name by determining the next element in the sequence
    fileName = getFileName(f"./images/{prefix}",prefix)
    
    
    # The image is embedded using a display.
    imageArray = [[0 for x in range(box.w)] for y in range(box.h)]
    for r in range(box.h):
        for c in range(box.w):
            pixel_r = box.y + r
            pixel_c = box.x + c
            # Add a padding of black pixels if the square get over the edges
            try:
                rgb = display.get_at((pixel_c,pixel_r))[0:3]
                # rgb = surface[pixel_r][pixel_c]
                bgr = rgb[::-1] #flip the rgb array to ensure it matches the default channel configuration from opencv
                imageArray[r][c] = bgr
            except:
                imageArray[r][c] = (0,0,0)
    imageAsArray = np.array(imageArray)
    # determine which dimension of the box is bigger, w vs h, then add padding accordingly
    if box.w > box.h:
        imageToSave = get_padded_image(imageAsArray,box.w)
    else:
        imageToSave = get_padded_image(imageAsArray,box.h)
    cv2.imwrite(fileName,imageToSave)
    print(fileName)
    # np.save("testIMG.npy",imageAsArray)