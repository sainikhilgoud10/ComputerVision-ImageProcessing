import cv2
from webcam import Webcam
class Detection(object):
    def __init__(self,webcaminstance):
        self.foundface =False
        self.webcam_instance = webcaminstance
    def is_face(self,cascade):
        self.cascade = cv2.CascadeClassifier(cascade)
        
        self.rects = self.cascade.detectMultiScale(self.webcam_instance.get_current_frame(),1.3,4,
                                              cv2.CASCADE_SCALE_IMAGE,(20,20))
        if len(self.rects) > 0:
            self.foundface = True
        else:
            self.foundface = False
        return self.foundface
    
    

    

            
        
            
            
            
