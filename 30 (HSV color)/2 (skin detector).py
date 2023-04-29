import cv2 as cv

video_cap = cv.VideoCapture(0, cv.CAP_DSHOW)

while True:
    ret, org_frame = video_cap.read()
    org_frame = cv.resize(org_frame, (0,0), fx=.5, fy=.5)
    height, width, _ = org_frame.shape
    
    frame = cv.cvtColor(org_frame, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(frame)
    for i in range (height):
        for j in range(width):
            if (30<h[i][j] and h[i][j]<175) or  s[i][j] < 40:
                org_frame[i][j] = (0,0,0)
                
    org_frame=cv.GaussianBlur(org_frame, (3,3),9)
    
    if cv.waitKey(1) == 115:
        cv.imwrite('heyo.jpg', org_frame)
        org_frame *= 0

    cv.imshow('h', org_frame)
