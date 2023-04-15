import argparse
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")    
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped




parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
args = parser.parse_args()

org_img = cv.imread(args.input)
img = cv.cvtColor(org_img, cv.COLOR_BGR2GRAY)
img = cv.GaussianBlur(img, (7,7), 3)
img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 17, 2)
# plt.imshow(img, 'gray')
# cv.imwrite('table2.jpg', img)





contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)



contours = sorted(contours, key=cv.contourArea, reverse=True)

for contour in contours:
    epsilon = .02 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        # cv.drawContours(org_img, [approx], -1, (0,255,0), 20)
        warped = four_point_transform(org_img, approx.reshape(4,2))
        print(approx[0])
        break
# plt.imshow(org_img)
cv.imwrite('res.jpg', warped)

