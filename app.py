from flask import Flask, render_template, Response, redirect, url_for,request, request
from flask_httpauth import HTTPBasicAuth
import cv2
from cam2 import VideoCamera
from flask import flash
from end_point import ulrs

user="admin"
user_password="1234"
camera = VideoCamera()

# this needs auth FLask httpauth
app = Flask(__name__)
motion_detected = False
app.secret_key = 'your_secret_key_here'


token = None

cam = VideoCamera()

@app.route(urls.get('Home'))
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')
        if camera.record_flag and camera.out is not None:
            camera.out.write(frame)

@app.route(urls.get('Stream'))
def video_feed():
    global cam
    if motion_detected:
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return 'Motion not detected'

@app.route('/motion_detected', methods=['POST'])
def set_motion_detected():
    global motion_detected
    data = request.get_json()
    motion_detected = data.get("motion_detected")
    print("motion", motion_detected)
    if motion_detected:
        cam = VideoCamera()
    return 'OK'

      
@app.route(urls.get('Login', methods=['GET', 'POST']), methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == user and password == user_password:
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')  # Flash an error message
            return redirect(url_for('login'))  # Redirect back to the login page

    return render_template('login.html')

@app.route(ulrs.get('Rec'))
def record():
    global cam
    cam.start_recording()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)