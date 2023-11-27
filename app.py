from flask import Flask, flash, render_template, Response, redirect, url_for, request, jsonify, session
from cam2 import VideoCamera
from end_point import urls
import os
from flask_cors import CORS
from passlib.hash import sha256_crypt
import secrets


#user credential
user="admin"
user_password="$5$rounds=535000$KPqyrKLnCS9IRv18$qr9KrAIBIkYIUQ8uJ1B8qWR5sb8SU3uT9WuHNfklO6B"

app = Flask(__name__, static_folder ='static')
app.config['SEND_FILE_MAX_RANGE'] = 0
CORS(app)

app.secret_key = secrets.token_hex(16)
motion_detected = False

cam = VideoCamera() #camera instance

@app.route(urls.get('Home')) # type: ignore
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

@app.route(urls.get('Stream')) # type: ignore
def video_feed():
        global cam
        if 'user' in session:
            cam.logged = True
        return Response(gen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/motion_detected', methods=['POST'])
def set_motion_detected():
    global motion_detected
    global cam
    data = request.get_json()
    motion_detected = data.get("motion_detected")
    print("motion", motion_detected)
    #if motion_detected:
        #cam = VideoCamera()
    
    cam.start_recording()
    return motion_detected

      
@app.route(urls.get('Login'), methods=['POST','GET']) # type: ignore
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(password)

        if username == user and sha256_crypt.verify(str(password),user_password):
            
            session['user'] = 'connected'

            return redirect(url_for('index'))
        else:
            flash("Wrong Credential")
            return redirect(url_for('login'))  # Redirect back to the login page

    return render_template('login.html')

@app.route(urls.get("Rec")) # type: ignore
def record():
    global cam
    if not cam.record_flag:
        cam.start_recording()
        print('recording!')
    return str(cam.out)

@app.route('/rec_portal')
def portal():
    if 'user' in session:
        return render_template('viewRecording.html')
    else:
        return render_template('login.html')

@app.route('/rec_info')
def get_info():

    if 'user' in session:

        dir_path = r'./static/video/'
        res = []
        pic = []

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path,path)):
                
                res.append({"vid_name":path})
                
        json_string = jsonify(res)
        return json_string
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True) # type: ignore