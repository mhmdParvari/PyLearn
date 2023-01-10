import numpy as np
import cv2 as cv

def NxN_convolution(img, n):
    mask = np.ones((n, n))
    mask /= n * n
    height, width = img.shape
    half = n//2
    for i in range(half, height - half):
        for j in range(half, width - half):
            img[i][j] = np.sum(img[i-half: i+half+1, j-half: j+half+1] * mask)
    return img

image = cv.imread('penguin.jpg', 0)
cv.imwrite('p1.jpg',NxN_convolution(image, 3))
cv.imwrite('p2.jpg',NxN_convolution(image, 5))
cv.imwrite('p3.jpg',NxN_convolution(image, 7))
cv.imwrite('p4.jpg',NxN_convolution(image, 15))


