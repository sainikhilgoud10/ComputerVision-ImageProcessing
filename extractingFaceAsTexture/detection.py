import cv2
from webcam import webcam
class detection(object):
    def __init__(self,webcamInstance):
        self.webcamInstance = webcamInstance
    def is_face(self,cascade):
        self.cascade = cv2.CascadeClassifier(cascade)
        self.rects = self.cascade.detectMultiScale(self.webcamInstance.getCurrentFrame(),1.3,4,
                                              cv2.CASCADE_SCALE_IMAGE,(20,20))
        return self.rects