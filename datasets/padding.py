import cv2
import numpy as np
from constants import * 

def pad_image(image, target_size, padding_type='black'):
    h, w = image.shape[:2]
    delta_w = target_size[1] - w
    delta_h = target_size[0] - h
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    
    if padding_type == 'black':
        color = [0, 0, 0]
        new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    elif padding_type == 'random':
        new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=np.random.randint(0, 256, size=3).tolist())
    elif padding_type == 'reflect':
        new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_REFLECT)
    elif padding_type == 'replicate':
        new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_REPLICATE)
    else:
        raise ValueError("Unsupported padding type")
    
    return new_image

# FD. get_added_image(str,int)
# purp. add padding to the image based on the padding_type:
# black
# random
# reflect   *Default
# replicate
def get_padded_image(image_to_pad,dim):
    padded_image = pad_image(image_to_pad, (dim, dim), padding_type=PADDING_TYPE)
    return padded_image
    
    
# if __name__ == "__main__":
#     padded_image = image = cv2.imread('./images/rotifer/rotifer_000000.png')
#     cv2.imshow('Padded Image', padded_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()