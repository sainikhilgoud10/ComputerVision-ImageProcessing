import pygame,sys;
import cv2;
import numpy as np;
from pygame.locals import *;
from OpenGL.GL import *
from OpenGL.GLU import *
class opencvGameClass(object):
    
    def settingUpTheDisplay(self):
        self._CamReaderObject = CamReader();
        pygame.init();
        display=(600,480)
        self._display = pygame.display.set_mode(display,pygame.DOUBLEBUF|OPENGLBLIT|pygame.OPENGL);
        gluPerspective(45,(display[0]/display[1]),0.1,50.0)
        glTranslatef(0.0,0.0,-5)
        glRotatef(0,0,0,0)
        pygame.display.set_caption('hello');
        self._manImg = pygame.image.load('ship.png');
        
    def gameLoop(self):
        while True:
            frame = self._CamReaderObject.getFrame();
            #self._framesize = self._CamReaderObject._frame.shape[1::-1];
            rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB);
            pygameFrame = pygame.image.frombuffer(rgbFrame.tostring(),self._CamReaderObject._frame.shape[1::-1],'RGB');
            self._display.blit(pygameFrame,(0,0));
            self._display.blit(self._manImg,(self._CamReaderObject.getPointX(),400));
            #pygame.draw.rect(self._display,(255,0,0),(self._CamReaderObject.getPointX(),420,80,60));
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.cube()

            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit();
                    sys.exit();
            pygame.display.update();
    def cube(self):
        vertices = (
            (1,-1,-1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (1,-1,1),
            (1,1,1),
            (-1,-1,1),
            (-1,1,1)
            )
        edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7),
            )
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
class CamReader(object):
    def __init__(self):
        self._frame = None;
        self._point = [0,0];
        self._capture = cv2.VideoCapture(0);
    def getPointX(self):
        return self._point[0];
    def getPointY(self):
        return self._point[1];
    def getFrame(self):
        success,self._frame = self._capture.read();
        hsv = cv2.cvtColor(self._frame,cv2.COLOR_BGR2HSV);
        lower_blue = np.array([110,50,50]);
        upper_blue = np.array([130,255,255]);
        #lower_blue = np.array([210,50,50]);
        #upper_blue = np.array([255,200,200]);
        mask = cv2.inRange(hsv,lower_blue,upper_blue);
        thresh = cv2.threshold(mask,25,255,cv2.THRESH_BINARY)[1];
        thresh = cv2.dilate(thresh.copy(),None,iterations = 2)
        res = cv2.bitwise_and(self._frame,self._frame,mask=mask);
        (_,cnts,_) = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);
        
        max_area = 25000;
        min_area = 10000;
        for i in range(len(cnts)):
            cnt = cnts[i];
            area = cv2.contourArea(cnt);
            if(area>min_area and area<max_area):
                ci = i;
                (x,y,w,h) = cv2.boundingRect(cnts[ci]);
                center = (int((x+w/2)),int((y+h/2)));
                print(center);
                self._point = list(center);
                cv2.rectangle(self._frame,(x,y),(x+w,y+h),(0,255,0),2);
                cv2.putText(self._frame,str(cv2.contourArea(cnts[ci])),(int((x+w/2)-0.65/2),int((y+h/2)-0.65/2)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,(0,0,255),1);
        return self._frame;
