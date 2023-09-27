from flask import Flask, render_template, Response, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import cv2
from cam2 import VideoCamera

# this needs auth FLask httpauth
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')

@app.route('/vid_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)