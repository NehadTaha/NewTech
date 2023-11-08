from flask import Flask, render_template, Response, redirect, url_for, request
import cv2
from cam2 import VideoCamera
from end_point import urls

# this needs auth FLask httpauth
app = Flask(__name__)

token = None

cam = VideoCamera()

@app.route(urls.get('Home'))
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame[0] +
               b'\r\n\r\n')
        if camera.record_flag and camera.out is not None:
            camera.out.write(frame[1])

@app.route(urls.get('Stream'))
def video_feed():
    global cam
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route(urls.get('Login'), methods=['POST','GET'])
def login():
    if request.method =='POST':
        data = request.form
    
    return render_template('login.html')

@app.route(urls.get('Rec'))
def record():
    global cam
    cam.start_recording()
    return 'hello world'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)