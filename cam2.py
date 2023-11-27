from tkinter import EXCEPTION
import cv2
import time
import threading
import datetime

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'MPV4') # type: ignore
        self.out = None
        self.record_flag = False
        self.logged = False

        
    def __del__(self):
        self.video.release()
        
    def get_frame(self):
        ret, frame = self.video.read()
        if not self.logged:
            _ = bytes()
            return (_,frame)
        else:
            ret, jpeg = cv2.imencode('.jpg',frame)
            return(jpeg.tobytes(),frame)
    
    def get_snapshot(self):
        #this could get a tumbnail
        ...
        #vid_for_snap = cv2
    
    def wait_time(self):
        time.sleep(10)
        if self.record_flag:
            self.stop_recording()
    
    def start_recording(self):
        name = str(datetime.datetime.now().strftime('%A-%b-%d-%Y-%H-%M-%S')) +'.mp4'
        print(name)
        self.out = cv2.VideoWriter('static/video/' + name , self.fourcc, 20.0, (640, 480))  
        self.record_flag = True
        try:
            t1 = threading.Thread(target=self.wait_time)
            t1.start()
        except Exception as error:
            print(str(error) + ' in start_rec')
            self.out.release()
            self.record_flag = None
        
        
    
    def stop_recording(self):
            try:

                if self.out is not None:
                    self.out.release()
                    self.out = None
                self.record_flag = False
                print('all done')
            except Exception as error:
                print(str(error) + ' in stop_rec')
                self.out.release() # type: ignore


        
    