import cv2
import time
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.record_flag = False
        
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        ret, frame = self.video.read()
        
        ret, jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes()
    
    def wait_time(self):
        time.sleep(10)
        stop_recording()
    
    def start_recording():
        self.out = cv2.VideoWriter('output.mp4', self.fourcc, 20.0, (640, 480))  
        self.record_flag = True
        t1 = threading.Thread(target=wait_time)
        t1.start()
        return 'all good'
    
    def stop_recording(): 
        if self.out is not None:
            self.out.release()
            self.out = None
        self.record_flag = False

        
    