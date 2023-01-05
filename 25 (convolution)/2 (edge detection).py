import numpy as np
import cv2 as cv

img = cv.imread('lion.png', 0)
height, width = img.shape
result = np.zeros(img.shape)
filter = np.array([[0, -1, 0],
                   [-1, 4, -1],
                   [0, -1, 0]])

for i in range(1, height-1):
    for j in range(1, width-1):
        result[i][j] = np.sum(img[i-1:i+2, j-1:j+2] * filter)

cv.imwrite('j.jpg',result)
