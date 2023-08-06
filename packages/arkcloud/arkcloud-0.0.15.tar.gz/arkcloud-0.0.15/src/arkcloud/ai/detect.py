import cv2
import numpy as np


def locate(image_item, base_image):
    base = cv2.imread(base_image, 0)
    item = cv2.imread(image_item, 0)

    res = cv2.matchTemplate(base, item, cv2.TM_SQDIFF)

    threshold = 0.5
    loc = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(min_loc, loc)

