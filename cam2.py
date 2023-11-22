import cv2
import time
import threading
import datetime

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
        return (jpeg.tobytes(),frame)
    
    def wait_time(self):
        time.sleep(10)
        self.stop_recording()
    
    def start_recording(self):
        name = str(datetime.datetime.now().strftime('%A-%b-%d-%Y-%H-%M-%S')) +'.mp4'
        print(name)
        self.out = cv2.VideoWriter('static/video/' + name , self.fourcc, 20.0, (640, 480))  
        self.record_flag = True
        t1 = threading.Thread(target=self.wait_time)
        t1.start()
    
    def stop_recording(self): 
        if self.out is not None:
            self.out.release()
            self.out = None
        self.record_flag = False

        
    