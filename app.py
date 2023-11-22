from flask import Flask, render_template, Response, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from cam2 import VideoCamera
from end_point import urls


# this needs auth FLask httpauth
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=60)], render_kw={"placeholder": "Email"})
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


motion_detected = False
app.secret_key = 'your_secret_key_here'

cam = VideoCamera()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +
               b'\r\n\r\n')
        if camera.record_flag and camera.out is not None:
            camera.out.write(frame)


@app.route(urls.get('Home'))
def index():
    return render_template('home.html', form=LoginForm())


@app.route(urls.get('Stream'))
@login_required
def video_feed():
    global cam
    if motion_detected:
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return 'Motion not detected'
    return render_template('login.html', form=form)

    


@app.route('/motion_detected', methods=['POST'])
def set_motion_detected():
    global motion_detected
    data = request.get_json()
    motion_detected = data.get("motion_detected")
    print("motion", motion_detected)
    if motion_detected:
        cam = VideoCamera()
    return 'OK'


@app.route(urls.get('Login'), methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('index.html')
        else:
            flash('Invalid credentials', 'error')  # Flash message for invalid credentials
    return render_template('login.html', form=form)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        
        username = request.form.get("username")
        password = request.form.get("password")

      
        username_exists = User.query.filter_by(username=username).first()

      
        if username_exists:
            print('Username is already in use.')
            flash('Username is already in use.', 'error')
           
        elif len(username) < 4:
            flash('Username is too short.', 'error')
        elif len(password) < 8:
            flash('Password is too short.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            # flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route(urls.get('Rec'))
@login_required
def record():
    global cam
    cam.start_recording()
    return redirect(url_for('login'))
 



if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
