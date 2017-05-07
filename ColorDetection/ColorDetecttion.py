import cv2;
from collections import deque;
import numpy as np;
cap = cv2.VideoCapture(0);
pts = deque(maxlen=10);
counter = 0;
(dX,dY) = (0,0);
#inRange = False;
while(1):
    #reading the frame
    _,frame = cap.read();

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV);
    #defining the required color
    lower_blue = np.array([110,50,50],dtype="uint8");
    upper_blue = np.array([130,255,255],dtype="uint8");
    #lower_blue = np.array([0,48,80],dtype = "uint8");
    #upper_blue = np.array([20,255,255],dtype="uint8");
    #masking and creating binary image from the detected color part
    mask = cv2.inRange(hsv,lower_blue,upper_blue);
    thresh = cv2.threshold(mask,25,255,cv2.THRESH_BINARY)[1];
    thresh = cv2.dilate(thresh.copy(),None,iterations = 2)
    #storing the extracted part of detected image as a result
    res = cv2.bitwise_and(frame,frame,mask=mask);
    #finding contours from the result
    (_,cnts,_) = cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE);
    #defining min and max area
    max_area = 25000;
    min_area = 1000;
    #max_area = 0;
    #detecting the required contour from the defind area constraints
    for i in range(len(cnts)):
        cnt = cnts[i];
        area = cv2.contourArea(cnt);
        
        if(area<max_area and area>min_area):
            #max_area = area;
            inRange = True;
            ci = i;
            (x,y,w,h) = cv2.boundingRect(cnts[ci]);
            print("height is ");
            print(h);
            #getting the center coordinate from rectangle
            center = (int((x+w/2)),int((y+h/2)));
            print(center);
            pts.appendleft(center);
            cv2.rectangle(frame,(x,y),
                          (x+w,y+h),(0,255,0),2);
            cv2.putText(frame,str(cv2.contourArea(cnts[ci])),(int((x+w/2)-0.65/2),int((y+h/2)-0.65/2)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,(0,0,255),1);
    for i in np.arange(1,len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue;
        thickness = int(np.sqrt(10/float(i+1))*2.5);
        cv2.line(frame,pts[i-1],pts[i],(0,0,255),thickness);
    cv2.imshow('result',res);
    cv2.imshow('frame',frame);
    #cv2.imshow('threshold',thresh);
    cv2.imshow('mask',mask);
    k=cv2.waitKey(5) & 0xFF;
    if k== 27:
        break;
    counter+=1;
cap.release();
cv2.destroyAllWindows();
