from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
from models import db, Session, UserTable, Comment, CommentSection, Post, Party, insert_BLOB_user, return_media, return_img, insert_BLOB_post
from dotenv import load_dotenv
import os
from datetime import datetime
from botocore.exceptions import ClientError
import sys
from time import time, sleep 
import boto3
from boto3 import logging
from bucket_wrapper import BucketWrapper
from thumbnail_generator import generate_thumbnail
from werkzeug.utils import secure_filename
from tinytag import TinyTag
import subprocess

# Load environment variables
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)
app.app_context().push()

app.config['MAX_CONTENT_LENGTH'] = 1_048_576 * 1_048_576
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.mov', '.mp3', '.png']
app.config['UPLOAD_PATH'] = 'static//uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

boto3.set_stream_logger('', logging.INFO)
logger = logging.getLogger()

# Create AWS session
session = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
            )

# Create clients from session
s3_client = session.client('s3')
s3_resource = session.resource('s3')
s3_distr = session.client('cloudfront')

# Get CloudFront distribution
distribution = s3_distr.get_distribution(Id="E2CLJ3WM17V7LF")

# URL for distribution, append object keys to url to access 
distribution_url = f'https://{distribution['Distribution']['DomainName']}/'

# Get specific bucket from s3
riff_bucket = s3_resource.Bucket('riffbucket-itsc3155')

# Wrap bucket to access specific funcionality
bucket_wrapper = BucketWrapper(riff_bucket)

@app.route('/')
def homepage():

    videos = bucket_wrapper.get_objects(s3_client) 

    return render_template('index.html', videos=videos, distribution_url=distribution_url)    

@app.get('/sessions')
def get_sessions():
    MAPS_API_KEY = os.getenv('MAPS_API_KEY') 
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_sessions = Session.query.all()

    session_data = []

    for i in active_sessions:
        result = i.serialize
        date_str = Session.date_str(result['date'])
        session_data.append(result)

    return render_template('sessions.html', current_date=current_date, max_date=max_date, active_sessions=active_sessions, session_data=session_data, date_str=date_str, MAPS_API_KEY=MAPS_API_KEY)

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

    s = Session(title, message, date, date_posted, lat, lng, 1)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('get_sessions'))

@app.post('/sessions/<int:session_id>/delete')
def delete_session(session_id: int):
    session = Session.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('get_sessions'))

@app.get('/sessions/<int:session_id>')
def get_single_session(session_id: int):
    session = Session.query.get(session_id)
    return render_template('get_single_session.html', session=session)

@app.route('/user_prof')
def user_prod():
    return None #rendertemplate('user_profile.html')

@app.route('/settings')
def settings_page():
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

    if filename:
        file_ext = os.path.splitext(filename)[1]        
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        #bucket_wrapper.add_object(file_name=filename, client=s3_client, object_id='NewUpload')
        #s3_client.upload_file(f'static/uploads/{filename}', 'riffbucket-itsc3155', 'videos/img.png')
        
        #generate_thumbnail(f'{app.config['UPLOAD_PATH']}/{filename}', app.config['UPLOAD_PATH'])
        msg = "File Uploaded" 
    return redirect(url_for('get_video', msg=msg))

