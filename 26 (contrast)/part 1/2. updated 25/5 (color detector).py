import numpy as np
import cv2 as cv

def modified_NxN_convolution(img, n):
    mask = np.ones((n, n))
    mask /= n * n
    height, width = img.shape
    result = np.zeros(img.shape, np.uint8)
    
    m = n//2
    center_y = height//2
    center_x = width//2
    for i in range(m, height - m):
        for j in range(m, width - m):
            if not (center_y-40 < i < center_y+40 and center_x-40 < j < center_x+40):
                result[i][j] = np.sum(img[i-m: i+m+1, j-m: j+m+1] * mask)
    t=35
    result[center_y-t : center_y+t+1, center_x-t : center_x+t+1] = img[center_y-t : center_y+t+1, center_x-t : center_x+t+1]
    
    return result

video_cap = cv.VideoCapture(0, cv.CAP_DSHOW)

while True:
    ret, frame = video_cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.resize(frame, (0,0), fx=.5, fy=.5)

    frame = modified_NxN_convolution(frame, 21)
    frame = cv.equalizeHist(frame)
    
    center_x = frame.shape[1]//2
    center_y = frame.shape[0]//2
    travel = 33

    if frame[center_y][center_x-travel] < 40 and frame[center_y][center_x+travel] < 40 and frame[center_y-travel][center_x] < 40 and frame[center_y+travel][center_x] < 40:
        cv.putText(frame,'Black',(10,40),cv.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),2)
    elif frame[center_y][center_x-travel] > 130 and frame[center_y][center_x+travel] > 130 and frame[center_y-travel][center_x] > 130 and frame[center_y+travel][center_x] > 130: 
        cv.putText(frame,'White',(10,40),cv.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),2)
    else:
        cv.putText(frame,'Gray',(10,40),cv.FONT_HERSHEY_SIMPLEX,1,(0, 0, 0),2)

    print(frame[center_y][center_x-travel],frame[center_y][center_x+travel],frame[center_y-travel][center_x],frame[center_y+travel][center_x])

    cv.imshow('h', frame)
    cv.waitKey(1)

