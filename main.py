# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 10:32:28 2018

@author: AvaksTeam
"""

import numpy as np
import cv2
import objects

video = str('videos/video1.mp4')
cap = cv2.VideoCapture(video)
bgsub = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #background subtractor
kernelOpen = np.ones((3,3),np.uint8)
kernelClose = np.ones((11,11),np.uint8)

w = cap.get(3) #width
h = cap.get(4) #height
mx = int(w/8)
my = int(h/8)

#all variables
font = cv2.FONT_HERSHEY_SIMPLEX
objectss = []
crossed = []
age = 0
death = 0
oid = 1
areaMin = 25
areaMax = 300
uplimit = int(h*0.9)
downlimit = int(h*0.25)
leftlimit = int(5*(w/16))
rightlimit = int(11*(w/16))
wid3 = 25
hei3 = 35
expected = 0
accur = 0

while(cap.isOpened()):
    ret, frame = cap.read() #frame read
    fgmask = bgsub.apply(frame) #subtractor use
    try:
        ret,imBin = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)   
        mask = cv2.morphologyEx(imBin,cv2.MORPH_OPEN, kernelOpen) #Opening
        mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernelClose) #Closing    
    except:
        print(' ')
        break
    
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #create contours
    for cunt in contours0:
        #cv2.drawContorus(frame,cunt,-1,(0,255,0), 3, 8)
        area = cv2.contourArea(cunt)
        if (area > areaMin and area < areaMax): #contours treshold check
            M = cv2.moments(cunt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cunt)
            
            new = True
            for i in objectss:
                if abs(x-i.getX()) <= wid3 and abs(y-i.getY()) <= hei3:
                #if i.getDeath() <= 1000:    
                    i.setAge()
                    new = False
                    i.updateCoords(cx,cy)
                    break
                else:
                    i.setDeath()
            if new == True:
                o = objects.MyObject(oid,cx,cy,age,death)
                objectss.append(o)
                oid += 1
                              
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            #img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
    
    #checking if object is a person to count
    for i in objectss:
        if i.getAge() > 15:
            if i not in crossed:
                if (i.getY()) >= downlimit and (i.getY()) <= uplimit:
                    crossed.append(i)
                    
    #show video and numbeer
    num = len(crossed)
    strin = str(num)
    cv2.putText(frame,strin,(mx,my),font,2,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow('Counter',frame)
    
    key = cv2.waitKey(30) & 0xff
    if key==27:
        break

cap.release() #realease video
cv2.destroyAllWindows() #close all openCV windows

if video == 'videos/video1.mp4':
    expected = 4
if video == 'videos/video2.mp4':
    expected = 25
if video == 'videos/video3.mp4':
    expected = 16
if video == 'videos/video4.mp4':
    expected = 23
if video == 'videos/video5.mp4':
    expected = 17
if video == 'videos/video6.mp4':
    expected = 27
if video == 'videos/video7.mp4':
    expected = 28
if video == 'videos/video8.mp4':
    expected = 22
if video == 'videos/video9.mp4':
    expected = 10
if video == 'videos/video10.mp4':
    expected = 22

if num >= expected:
    accur = (float(expected)/num)*100
else:
    accur = (float(num)/expected)*100

print accur,'% accuracy'