import numpy as np
import cv2 as cv

img = cv.imread('flower_input.jpg', 0)
height, width = img.shape

mask = np.ones((21,21))
mask /= 441

for i in range(10, height-10):
    for j in range(10, width-10):
        if img[i][j] < 125:
            img[i][j] = np.sum(img[i-10:i+11, j-10:j+11] * mask)

cv.imwrite('flower_js.jpg',img)