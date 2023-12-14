from flask import Blueprint, render_template, redirect, url_for, request, abort, session, flash, current_app
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_bcrypt import bcrypt
from models import db, UserTable, JamSession, Party,Post
from flask import current_app
from bucket_wrapper import BucketWrapper
import boto3
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont




load_dotenv()

profile_bp = Blueprint('profiles', __name__, template_folder='templates', static_url_path='/static')


#Create AWS session
aws = boto3.Session(
                aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
            )

# Create clients from session
s3_client = aws.client('s3')
s3_resource = aws.resource('s3')
s3_distr = aws.client('cloudfront')
s3_transcoder = aws.client('elastictranscoder', 'us-east-1')

# Get CloudFront distribution
distribution = s3_distr.get_distribution(Id="E2CLJ3WM17V7LF")

# URL for distribution, append object keys to url to access 
distribution_url = f'https://{distribution["Distribution"]["DomainName"]}/'

# Get specific bucket from s3
riff_bucket = s3_resource.Bucket('riffbucket-itsc3155')

# Wrap bucket to access specific funcionality
bucket_wrapper = BucketWrapper(riff_bucket)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/upload', methods=['POST'])
def upload_profile_photo():
    if not session.get('id'):
        return redirect('/login')

    uploaded_file = request.files['file']
    if uploaded_file.filename == '' or not allowed_file(uploaded_file.filename):
        flash('Invalid file type or no file selected', 'error')
        return redirect(url_for('profiles.get_settings'))


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
            filename.save(file_path)

            user = UserTable.query.get(user_id)
            user.profile_photo_path = file_path
            db.session.commit()

            print("Uploaded file received:", filename)
            print("Is file allowed:", allowed_file(filename))
            flash('Profile photo uploaded successfully', 'success')

    return redirect(url_for('profiles.get_settings'))