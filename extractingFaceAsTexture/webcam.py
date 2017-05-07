import cv2
from threading import Thread
class webcam(object):
    def __init__(self):
        self.videoCapture = cv2.VideoCapture(0)
        self.currentFrame = self.videoCapture.read()[1]
    def start(self):
        Thread(target=self.updateFrame,args=()).start()
    def updateFrame(self):
        self.currentFrame = self.videoCapture.read()[1]
    def getCurrentFrame(self):
        return self.currentFrame
