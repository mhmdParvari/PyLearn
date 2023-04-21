import numpy as np
import cv2 as cv

def color_code(pixel):
    code = [-1,-1,-1]
    if pixel[0] > 110: code[0] = 1
    if pixel[0] < 60: code[0] = 0
    if pixel[1] > 110: code[1] = 1
    if pixel[1] < 60: code[1] = 0
    if pixel[2] > 110: code[2] = 1
    if pixel[2] < 60: code[2] = 0
    return code

video_cap = cv.VideoCapture(0, cv.CAP_DSHOW)
while True:
    ret, org_frame = video_cap.read()
    # org_frame = cv.cvtColor(org_frame, cv.COLOR_BGR2GRAY)
    # org_frame = cv.resize(org_frame, (0,0), fx=.5, fy=.5)
    mask = np.ones((27,27))
    mask /= 27 * 27
    frame = cv.filter2D(org_frame, -1, mask)
    t=60
    center_x = frame.shape[1]//2
    center_y = frame.shape[0]//2
    frame[center_y-t : center_y+t+1, center_x-t : center_x+t+1] = (0,0,0)
    t=50
    target = org_frame[center_y-t : center_y+t+1, center_x-t : center_x+t+1]
    frame[center_y-t : center_y+t+1, center_x-t : center_x+t+1] = target
    # frame = modified_NxN_convolution(frame, 21)
    # b,g,r = cv.split(frame)
    # b = cv.equalizeHist(b)
    # g = cv.equalizeHist(g)
    # r = cv.equalizeHist(r)
    # clah = cv.createCLAHE(4,(8,8))
    # b = clah.apply(b)
    # g = clah.apply(g)
    # r = clah.apply(r)

    # frame = cv.merge((b,g,r))
    
    # travel = 33

    avg_pixel = np.mean(np.mean(target, 0), 0)
    avg_pixel = [int(p) for p in avg_pixel]
    code = color_code(avg_pixel)
    # print(code)
    if code == [0,0,0]: color_name = 'Black'
    if code == [1,1,1]: color_name = 'White'
    if code == [-1,-1,-1]: color_name = 'Gray'
    if code == [1,0,0] or code == [1,-1,-1]: color_name = 'Blue'
    if code == [0,1,0] or code == [-1,1,-1]: color_name = 'Green'
    if code == [0,0,1] or code == [-1,-1,1]: color_name = 'Red'
    if code == [1,1,0] or code == [1,1,-1]: color_name = 'Firouzei'
    if code == [0,1,1] or code == [-1,1,1]: color_name = 'Yellow'
    if code == [1,0,1] or code == [1,-1,1]: color_name = 'Purple'

    cv.putText(frame, color_name, (10,70), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)

    
    if cv.waitKey(1) == 115:
        cv.imwrite('heyyyyoo.jpg', frame)
        frame *= 0

    cv.imshow('h', frame)
