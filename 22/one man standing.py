import random
import numpy as np
import cv2 as cv

########## 1 ########
img1 = cv.imread('assets/a.tif')
img2 = cv.imread('assets/b.tif')
result = cv.subtract(img2, img1)
cv.imwrite('sokhan bozorgan.jpg', result)

############ 2 #############
def reduce_noise(images=[]):
    result=np.zeros((images[0].shape),np.uint8)
    for image in images:
        result += image // len(images)
    return result
part =[]
for i in range(1,5):
    images =[]
    for j in range(1,6):
        images.append(cv.imread(f'assets/black hole/{i}/{j}.jpg',0))
    part.append(reduce_noise(images))
top_part = np.c_[part[0],part[1]]
bottom_part = np.c_[part[2],part[3]]
whole_image = np.r_[top_part, bottom_part]
cv.imwrite('ss.jpg', whole_image)


########### 3 ###########
test_img = cv.imread('assets/board - test.bmp')
test_img = cv.flip(test_img,1)
original_img = cv.imread('assets/board - origin.bmp')
error_img = cv.subtract(test_img, original_img)
cv.imwrite('ssa.jpg', error_img)

######## 4 ###########
images =[]
for i in range(0,15):
    images.append(cv.imread(f'assets/highway/h{i}.jpg',0))
images.append(images[0])
images.append(images[0])
images.append(images[0])
images.append(images[0])
images.append(images[0])
images.append(images[0])
images.append(images[0])
images.append(images[0])

cv.imwrite('highW.jpg',reduce_noise(images))

########## 5 #########
img1 = cv.imread('assets/ostad.jpg', 0)
img2 = cv.imread('assets/linus.jpg', 0)
img2 = cv.resize(img2,(640,640))
merge1 = img1//10*6 + img2//10*4
merge2 = img2//10*6 + img1//10*4

# final_img=np.zeros((640,2560),np.uint8)
# final_img[0:640,0:640]=img1
# final_img[0:640,640:1280]=merge1
# final_img[0:640,1280:1920]=merge2
# final_img[0:640,1920:2560]=img2

final_img = np.c_[img1, merge1, merge2, img2]

cv.imwrite('z.jpg',final_img)

######### 6 #############
image = cv.imread('assets/Mona_Lisa.jpg', 0)
inverted = 255 - image
blurred = cv.GaussianBlur(inverted, (21,21), 0)
inverted_blurred = 255 - blurred
sketch = image / inverted_blurred * 255
cv.imwrite('ask.jpg',sketch)

############ 7 ###########
image = cv.imread('assets/chess pieces.jpg', 0)
height, width = image.shape
noise_intensity = 10
for i in range(noise_intensity * 100):
    col = random.randint(0, width-1)
    row = random.randint(0, height-1)
    if image[row][col] < 50:
        image[row][col] = 255
    elif image[row][col] > 180:
        image[row][col] = 0
cv.imwrite('noisy.jpg',image)

cv.waitKey()
