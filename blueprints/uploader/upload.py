from flask import Blueprint, flash, render_template, redirect, url_for, request, abort, session
from dotenv import load_dotenv
import os
from datetime import datetime
from models import db, Post
from werkzeug.utils import secure_filename
from flask import current_app
import boto3
from bucket_wrapper import BucketWrapper
from blueprints.uploader.thumbnail_generator import generate_thumbnail
from uuid import uuid4
from time import sleep
from models import db, UserTable, Comment, CommentSection, Party, Post, insert_BLOB_user


load_dotenv()

upload_bp = Blueprint('upload', __name__, template_folder='templates', static_folder='static')


aws = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
            ) 

s3_client = aws.client('s3')
s3_resource = aws.resource('s3')
s3_transcoder = aws.client('elastictranscoder', 'us-east-1')

upload_bucket = s3_resource.Bucket('riffbucket-itsc3155-upload')

upload_bucket_wrapper = BucketWrapper(upload_bucket)

stashed_files = []

@upload_bp.get('/')
def get_upload_page():
    if not session.get('id'):
        return redirect('/login')
    
    if stashed_files:
        for f in stashed_files:
            remove_file(f)
    
    return render_template('upload_video.html')


@upload_bp.post('/new')
def upload_video():
    if not session.get('id'):
        return redirect('/login')
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]        
        if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
            abort(400)

        title = request.form.get('title')
        message = request.form.get('description')

        current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')

        file_key = str(uuid4())

    # Production path
        if current_app.config['FLASK_ENV'] == 'prod':
        
            post = Post(video_id=file_key, title=title, msg=message, ratio=0, date=current_date, user_id=session.get('id'))

            db.session.add(post)
            
            uploaded_file.save(os.path.join('static/uploads', filename))
            upload_bucket_wrapper.add_object(s3_client, f'{current_app.config["UPLOAD_PATH"]}/{filename}', filename)

            response = s3_transcoder.create_job(
                PipelineId = current_app.config["PIPELINE_ID"],
                Input={
                    'Key': f'{filename}',
                    'FrameRate': 'auto',
                    'Resolution': 'auto',
                    'AspectRatio': 'auto',
                    'Interlaced': 'auto',
                    'Container': 'auto',
                },
                Output={
                    'Key': f'{file_key}.mp4',
                    'ThumbnailPattern': 'thumbnails/' + file_key + '-{count}',
                    'Rotate': 'auto',
                    'PresetId': '1351620000001-000010',
                },
                OutputKeyPrefix='videos/'
            )

            
            db.session.commit()

            remove_file(filename)
            
            return redirect(url_for('upload.get_upload_page'))
    # Development Path
        else:
            post = Post(video_id=file_key, title=title, msg=message, ratio=0, date=current_date, user_id=session.get('id'))
            
            db.session.add(post)
        
            uploaded_file.save(os.path.join('static/uploads/videos/', f'{file_key}.mp4'))
            generate_thumbnail(f'{current_app.config["UPLOAD_PATH"]}/videos/{file_key}.mp4', f'{current_app.config["UPLOAD_PATH"]}/thumbnails/')

            db.session.commit()
        return redirect(url_for('upload.get_upload_page'))


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/profile/upload', methods=['POST'])
def upload_profile_photo():
    if not session.get('id'):
        return redirect('/login')

    uploaded_file = request.files['file']
    if uploaded_file.filename == '' or not allowed_file(uploaded_file.filename):
        flash('Invalid file type or no file selected', 'error')
        return redirect(url_for('settings_page'))

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        user_id = session.get('id')

        # Prod path
        if current_app.config['FLASK_ENV'] == 'prod':
            # idk how to do this lol
            pass  

        # Dev path
        else:
            file_path = os.path.join('static/uploads/pfps/', f'{user_id}.jpg')
            uploaded_file.save(file_path)

            user = UserTable.query.get(user_id)
            user.profile_photo_path = file_path
            db.session.commit()

            flash('Profile photo uploaded successfully', 'success')

    return redirect(url_for('settings_page'))



def remove_file(filename):
    max_remove_attempts = 5
    attempts = 0
    removed = False
    while not removed or attempts > max_remove_attempts:
        try:
            os.remove(f'{current_app.config["UPLOAD_PATH"]}/{filename}')
            removed = True
            print("% s removed successfully" % filename)
        except OSError as error:
            print(error)
            print('Filepath cannot be removed.')
        else:
            if attempts == 5:
                stashed_files.append(filename)
            print(f'Removal attempt number {attempts}')
            attempts += 1
            sleep(3)
