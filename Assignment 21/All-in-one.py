import numpy as np
import math
import cv2 as cv

################## 1 ######################
chess = np.zeros((800,800), np.uint8)
for i in range(8):
    for j in range(8):
        if (i+j)%2 == 0:
            chess[i*100:(i+1)*100, j*100:(j+1)*100] = 255
cv.imshow('chess board', chess)

##############  2   ########################################
img = cv.imread('1.jpg',0)
height, width = img.shape
img = 255-img
cv.imshow('omg',img)

############# 3 ###############################
img = cv.imread('3.jpg',0)
height, width = img.shape
for i in range(math.ceil(height/2)):
    for j in range(width if i != height-1-i else int(width/2)):
        img[i][j] , img[height-1-i][width-1-j] = img[height-1-i][width-1-j] , img[i][j] 
cv.imshow('happ now?',img)

############### 4 ##########################
img = cv.imread('4.jpg',0)
height, width = img.shape
threshold = 160
for i in range(height):
    for j in range(width):
        if img[i][j] < threshold:
            img[i][j] = 0

cv.imshow('wolf',img)

################ 5 #################
img = cv.imread('dostoevsky.jpg')
thickness = 30
i=0
for j in range(100,-1,-1):
    img[i,j:j+thickness] = 0
    i+=1
for j in range(thickness-1,-1,-1):
    img[i,0:j] = 0
    i+=1
cv.imshow('rip', img)

################ 6 ###############3
shade = np.zeros((512,512), np.uint8)
color = 255
height, width = shade.shape
step = int(height / 256)
for i in range(0, height-1, step):
    shade[i:i+step, 0:width] = color
    color -= 1
cv.imshow('shadow', shade)

############## 7 ####################
name = np.zeros((512,512), np.uint8)
length = 100
i, j = int(name.shape[0]/2 - (length/2)), int(name.shape[1]/2- 40)
name = name + 255
thickness = 20
name[i:i+length, j:j+thickness] = 0

for row in range(i, i+length, 2):
    name[row,j:j+thickness] = 0
    name[row+1,j:j+thickness] = 0
    j+=1
for row in range(i+length-2, i-1, -2):
    name[row,j:j+thickness] = 0
    name[row-1,j:j+thickness] = 0
    j+=1
name[i:i+length, j:j+thickness] = 0

cv.imshow('first letter',name)

################ surprize ##############
chess = [[255,0,255,0,255,0,255,0],
        [0,255,0,255,0,255,0,255],
        [255,0,255,0,255,0,255,0],
        [0,255,0,255,0,255,0,255],
        [255,0,255,0,255,0,255,0],
        [0,255,0,255,0,255,0,255],
        [255,0,255,0,255,0,255,0],
        [0,255,0,255,0,255,0,255]]
chess = np.array(chess, np.uint8)
cv.imshow('sus chess', cv.resize(chess,(800,800)))

cv.waitKey()