from flask import Flask, flash, render_template, redirect, url_for, request, abort, jsonify, session
from models import db, JamSession, UserTable, Comment, CommentSection, Post, Party, insert_BLOB_user, return_media, return_img, insert_BLOB_post
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import sys
from time import time, sleep 
import boto3
from boto3 import logging
from bucket_wrapper import BucketWrapper
from thumbnail_generator import generate_thumbnail
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask_bcrypt import Bcrypt
from flask_session import Session

# Load environment variables
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)
app.app_context().push()

bcrypt = Bcrypt(app)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.permanent_session_lifetime = timedelta(minutes=30)

app.config['MAX_CONTENT_LENGTH'] = 1_048_576 * 1_048_576
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.mov', '.mp3']
app.config['UPLOAD_PATH'] = 'static//uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

boto3.set_stream_logger('', logging.INFO)
logger = logging.getLogger()

# Create AWS session
aws_session = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
            )

# Create clients from session
s3_client = aws_session.client('s3')
s3_resource = aws_session.resource('s3')
s3_distr = aws_session.client('cloudfront')

# Get CloudFront distribution
distribution = s3_distr.get_distribution(Id="E2CLJ3WM17V7LF")

# URL for distribution, append object keys to url to access 
distribution_url = f'https://{distribution['Distribution']['DomainName']}/'

# Get specific bucket from s3
riff_bucket = s3_resource.Bucket('riffbucket-itsc3155')
upload_bucket = s3_resource.Bucket('riffbucket-itsc3155-upload')

# Wrap bucket to access specific funcionality
bucket_wrapper = BucketWrapper(riff_bucket)
upload_bucket_wrapper = BucketWrapper(upload_bucket)


@app.route('/')
def homepage():

    if not session.get('id'):
        return redirect('/login')
    
    print(f'Logged in as {UserTable.query.get(session.get('id')).user_name}')

    videos = bucket_wrapper.get_objects(s3_client) 

    return render_template('index.html', videos=videos, distribution_url=distribution_url)    

@app.get('/sessions')
def get_sessions():
    if not session.get('id'):
        return redirect('/login')

    MAPS_API_KEY = os.getenv('MAPS_API_KEY') 
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_jam_sessions = JamSession.query.all()

    jam_session_data = []

    for i in active_jam_sessions:
        result = i.serialize
        date_str = JamSession.date_str(result['date'])
        jam_session_data.append(result)

    return render_template('sessions.html', current_date=current_date, max_date=max_date, active_jam_sessions=active_jam_sessions, jam_session_data=jam_session_data, date_str=date_str, MAPS_API_KEY=MAPS_API_KEY)

@app.post('/sessions')
def add_new_session():
    data = request.get_json()
    title = data['title']

    if title is None or title == '':
        abort(400)

    message = data['message']

    lat = data['lat']
    lng = data['lng']

    if lat is None or lat == '' or lng is None or lng == '':
        abort(400)

    date = data['date']

    if date is None or date == '':
        abort(400)

    date_posted = datetime.now().strftime('%Y-%m-%dT%H:%M')

    s = JamSession(title, message, date, date_posted, lat, lng, 1)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('get_sessions'))

@app.post('/sessions/<int:jam_session_id>/delete')
def delete_session(session_id: int):
    session = JamSession.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('get_sessions'))

@app.get('/sessions/<int:session_id>')
def get_single_session(session_id: int):
    session = JamSession.query.get(session_id)
    return render_template('get_single_session.html', session=session)

@app.route('/user_prof')
def user_prof():
    return None #rendertemplate('user_profile.html')

@app.route('/settings')
def settings_page():
    if not session.get('id'):
        return redirect('/login')

    profile_pic_path = 'profile_pic.jpg'
    if os.path.exists(profile_pic_path):
        profile_pic_url = '/' + profile_pic_path
    else:
        profile_pic_url = '/static/default_pfp.jpg'
    return render_template('settings.html',  profile_pic_url=profile_pic_url)

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    file = request.files['profile_pic']
    file.save('profile_pic.jpg')  
    return redirect(url_for('settings_page'))

@app.get('/upload')
def get_video():
    return render_template('upload_video.html')

@app.post('/upload/new')
def upload_video():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]        
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        generate_thumbnail(f'{app.config['UPLOAD_PATH']}/{filename}', app.config['UPLOAD_PATH'])
    return redirect(url_for('get_video'))

@app.get('/login')
def get_login():
    if session.get('id'):
        return redirect('/')
    try:
        current_user = UserTable.query.get(session.get('id'))

        if session.get('id') == current_user.id:
            redirect(url_for('homepage'))
    except Exception as e:
        print(e)


    return render_template('login.html')

@app.post('/login')
def login():
        try:
            username = request.form.get('username')

            if not username or username == '':
                flash('Enter a username')
                return redirect(url_for('get_login'))
            
            raw_password = request.form.get('password')

            if not raw_password or raw_password == '':
                flash('Enter a password')
                return redirect(url_for('get_login'))

            current_user = UserTable.query.filter_by(user_name=username).first()

            if current_user:
                check_pass = bcrypt.check_password_hash(current_user.password, raw_password)
            
            if not check_pass:
                flash('Incorrect Username or Password')
                return redirect(url_for('get_login'))
        
            session['id'] = current_user.id

            flash('Successfully Logged In')
            return redirect(url_for('homepage'))
        except:
            sleep(3)
            flash('Incorrect Username or Password')
            return redirect(url_for('get_login'))
        

@app.post('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('get_login'))
    except Exception as e:
        print(e)
        return redirect(url_for('homepage'))
    
    


@app.post('/signup')
def sign_up():

    try:
        username = request.form.get('username')

        if not username or username == '':
            flash('Enter a username')
            return redirect(url_for('get_login'))
        
        raw_password = request.form.get('password')

        if not raw_password or raw_password == '':
            flash('Enter a password')
            return redirect(url_for('get_login'))

        hashed_password = bcrypt.generate_password_hash(raw_password, 16).decode()

        new_user = UserTable('John', 'Doe', username, hashed_password, 'johnd@gmail.com', 111_222_3333)
        db.session.add(new_user)
        db.session.commit()

        session['id'] = new_user.id
    
        flash('Successfully Signed Up')
        return redirect(url_for('homepage'))
    except:
        flash('Unable to Sign Up\nTry Again Later.')
        return redirect(url_for('get_login'))


