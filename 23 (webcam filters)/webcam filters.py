import cv2 as cv
import numpy as np
face_sticker = cv.imread('assets/ez.png')
lip_sticker = cv.imread('assets/laugh.png')
eye_sticker = cv.imread('assets/mason_eye.png')

face_detector = cv.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
smile_detector = cv.CascadeClassifier('assets/haarcascade_smile.xml')
eye_detector = cv.CascadeClassifier('assets/haarcascade_eye.xml')

def make_background_transparent(img, back_img):
    height, width, _ = back_img.shape
    img = cv.resize(img, (width, height))
    roi = back_img[0:height, 0:width]

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img_gray, 10, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)
    back_img_bg = cv.bitwise_and(roi,roi,mask = mask_inv)
    img_fg = cv.bitwise_and(img, img, mask = mask)

    return cv.add(back_img_bg, img_fg)

def ripbozo(img):
    i = 0
    thickness = 30
    for j in range(100,-1,-1):
        img[i,j:j+thickness] = 0
        i+=1
    for j in range(thickness-1,-1,-1):
        img[i,0:j] = 0
        i+=1

video_cap = cv.VideoCapture(0, cv.CAP_DSHOW)
filter = 0
while True:
    ret, frame = video_cap.read()
    if not ret: break
    
    if filter == 1:
        faces = face_detector.detectMultiScale(frame)
        for (x,y,w,h) in faces:
            frame[y:y+h, x:x+w] = make_background_transparent(face_sticker, frame[y:y+h, x:x+w])

    if filter == 2:
        eyes = eye_detector.detectMultiScale(frame, 1.2,minSize=(41,41),minNeighbors=8)
        smiles = smile_detector.detectMultiScale(frame,1.3,minNeighbors=24)
        for (sx,sy,sw,sh) in eyes:
            frame[sy:sy+sh, sx:sx+sw] = make_background_transparent(eye_sticker, frame[sy:sy+sh, sx:sx+sw])

        for (x,y,w,h) in smiles:
            frame[y:y+h, x:x+w] = make_background_transparent(lip_sticker, frame[y:y+h, x:x+w])
        
    if filter == 3:
        faces = face_detector.detectMultiScale(frame)
        for (x,y,w,h) in faces:
            temp = cv.resize(frame[y:y+h, x:x+w],(20,20))
            frame[y:y+h, x:x+w] = cv.resize(temp,(w,h),interpolation=cv.INTER_AREA)

    if filter == 4:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ripbozo(frame)

    cv.imshow('lol.jpg',frame)
    key=cv.waitKey(50)
    if key == 49: filter = 1
    if key == 50: filter = 2
    if key == 51: filter = 3
    if key == 52: filter = 4
    if key == 48 or key == 53: filter = 0
