#!/usr/bin/env python
import freenect
import cv2
import frame_convert2

cv2.namedWindow('Depth')
cv2.namedWindow('RGB')
keep_running = True


def display_depth(dev, data, timestamp):
    global keep_running
    myImg = frame_convert2.pretty_depth_cv(data)
    myImg = cv2.erode(myImg,None,iterations=5)
    myImg = cv2.dilate(myImg,None,iterations=5)
##    cv2.imshow('Depth', myImg)
    depthColorLower = (100)
    depthColorHigher = (150)
    mask = cv2.inRange(myImg, depthColorLower, depthColorHigher)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
##    bbox = (287, 23, 86, 320)
##    if len(cnts) > 0:
##        c = max(cnts, key=cv2.contourArea)
##        if ok:
##            p1 = (int(bbox[0]), int(bbox[1]))
##            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
##            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    c=max(cnts,key=cv2.contourArea)
    x,y,w,h=cv2.boundingRect(c)
    if(w > h):
        print("width is bigger")
    else:
        print("height is bigger")
        
    cv2.rectangle(myImg,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("Tracking", mask)
    cv2.imshow('depth',myImg)
    
    if cv2.waitKey(10) == 27:
        keep_running = False


def display_rgb(dev, data, timestamp):
    global keep_running
    #cv2.imshow('RGB', frame_convert2.video_cv(data))
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill


print('Press ESC in window to stop')
freenect.runloop(depth=display_depth,
                 video=display_rgb,
                 body=body)
