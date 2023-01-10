import numpy as np
import cv2 as cv

img = cv.imread('building.tif', 0)
height, width = img.shape
result1 = np.zeros(img.shape)
result2 = np.zeros(img.shape)

filter1 = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]])

filter2 = np.array([[-1, -1, -1],
                    [0, 0, 0],
                    [1, 1, 1]])

for i in range(1, height-1):
    for j in range(1, width-1):
        result1[i][j] = np.sum(img[i-1:i+2, j-1:j+2] * filter1)
        result2[i][j] = np.sum(img[i-1:i+2, j-1:j+2] * filter2)


cv.imwrite('build_1.jpg',result1)
cv.imwrite('build_2.jpg',result2)

