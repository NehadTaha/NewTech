import subprocess
import cv2
import time
import threading
import datetime

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'avc1') # type: ignore
        self.out = None
        self.record_flag = False
        self.logged = True
        self.f_name = ''
        
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
        try:
            self.f_name = str(datetime.datetime.now().strftime('%A-%b-%d-%Y-%H-%M-%S')) +'.mp4'
            print(self.f_name)
            self.out = cv2.VideoWriter('static/video/' + self.f_name , self.fourcc, 15.0, (640, 480))  
            self.record_flag = True
            t1 = threading.Thread(target=self.wait_time)
            t1.start()
        except Exception as error:
            print(str(error) + ' in start_rec')
            self.out.release()
            self.record_flag = None
            
    def convert_to_mp4(self):
        iao_file = self.f_name
        folder = "static/video/"
        
        ffmpeg_command=[
        "ffmpeg",
        "-i",
        folder + iao_file,
        "-vcodec",
        "libx264",
        "-acodec",
        "aac",
        folder + iao_file
        ]
        
        try:
            result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print("FFmpeg Output:\n", result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            print("FFmpeg Output:\n", e.stdout)
            print("FFmpeg Error Output:\n", e.stderr)
    
    def stop_recording(self):
            try:

                if self.out is not None:
                    self.out.release()
                    self.out = None
                self.record_flag = False
                print('all done')
                #time.sleep(2)
                #self.convert_to_mp4()
            except Exception as error:
                print(str(error) + ' in stop_rec')
                self.out.release() # type: ignore

    
