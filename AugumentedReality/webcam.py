import cv2
from threading import Thread
class Webcam:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
    def start(self):
        Thread(target=self._update_frame,args=()).start()
    def _update_frame(self):
        while(True):
            self.current_frame = self.video_capture.read()[1]
            #cv2.imshow('facedetect',self.current_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                #cv2.destroyAllWindows()
                self.video_capture.release()           
                quit()
    def get_current_frame(self):
        return self.current_frame
        
