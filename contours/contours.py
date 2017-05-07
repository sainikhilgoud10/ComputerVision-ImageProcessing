import cv2;
import numpy;
cap  = cv2.VideoCapture(0);
while (cap.isOpened()):
    ret,image = cap.read();
    #hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV);
        #lower_blue = np.array([110,50,50]);
        #upper_blue = np.array([130,255,255]);
    #lower_blue = numpy.array([110,50,50]);
    #upper_blue = numpy.array([130,255,255]);
    #mask = cv2.inRange(hsv,lower_blue,upper_blue);
    #thresh = cv2.threshold(mask,25,255,cv2.THRESH_BINARY)[1];
    #thresh = cv2.dilate(thresh.copy(),None,iterations = 2)
    #res = cv2.bitwise_and(image,image,mask=mask);
    #(_,contours,_) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);
    #blur = cv2.GaussianBlur(gray,(5,5),0);
    blur = cv2.medianBlur(gray,19);
    blur = cv2.medianBlur(blur,19);
    ret,thres = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU);
    img,contours,hirerchy = cv2.findContours(thres,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);

    drawing = numpy.zeros(image.shape,numpy.uint8);
    max_area = 110000;
    min_area = 60000;
    for i in range(len(contours)):
        cnt = contours[i];
        area = cv2.contourArea(cnt);
        if(area<max_area and area>min_area):
            #max_area = area;
            ci = i;
            cnt = contours[ci];
            hull = cv2.convexHull(cnt);
            moments = cv2.moments(cnt);
            if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']);
                cy = int(moments['m01']/moments['m00']);
                center = (cx,cy);
                cv2.putText(image,str(cv2.contourArea(cnt)),(cx,cy),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,(0,0,255),2);
    #help(cv2.circle);
                cv2.circle(image,center,5,(0,0,255),3,cv2.LINE_AA);
            cv2.drawContours(drawing,[cnt],0,(0,255,0),2);
            cv2.drawContours(drawing,[hull],0,(0,0,255),2);
            cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True);
            hull = cv2.convexHull(cnt,returnPoints=False);
    
            if(1):
                defects = cv2.convexityDefects(cnt,hull);
        #help(defects);
                mind = 0;
                maxd = 0;
                try:
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0];
                        start = tuple(cnt[s][0]);
                        end = tuple(cnt[e][0]);
                        far = tuple([cnt][0]);
                        dist = cv2.pointPolygonTest(cnt,center,True);
                        cv2.line(image,start,end,[0,255,0],2);
                        #cv2.circle(image,far,5,(0,0,255),-1,cv2.LINE_AA);
                        print(i);
                        i=0;
                except:
                    print("error");
                    break;
    cv2.imshow('window',drawing);
    cv2.imshow('input',image);
    cv2.imshow('blur',blur);
    k = cv2.waitKey(10);
    if k==27:
        break;
cap.release();
cv2.destroyAllWindows();
