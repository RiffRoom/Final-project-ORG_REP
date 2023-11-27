from flask import Blueprint, render_template, redirect, url_for, request, abort, session, flash
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_bcrypt import bcrypt
from models import db, UserTable, JamSession, Party
from flask import current_app
from bucket_wrapper import BucketWrapper
import boto3

load_dotenv()

profile_bp = Blueprint('profiles', __name__, template_folder='templates')


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



@profile_bp.get('/')
def get_profile():
    # get profile page
    pass

@profile_bp.get('/settings')
def get_settings():
    if not session.get('id'):
        return redirect('/login')


    if current_app.config['FLASK_ENV'] == 'prod':
        pfp = bucket_wrapper.get_object(s3_client, f'{current_app.config["PFP_PATH"]}testpfp.png')

    current_user = UserTable.query.get(session.get('id'))

    if session.get('id') == current_user.id:
        print(current_user)
        print(current_user.id)


    pfps = bucket_wrapper.get_objects(s3_client) 
    print(pfps)
    print(f'{distribution_url}{pfps[0]}/images/pfp/testpfp.png')

    return render_template('settings.html', profile_pic_url=pfps, distribution_url=distribution_url, private_setting=current_user.private)


# To view another users profile
@profile_bp.get('/<int:user_id>')
def view_profile(user_id: int):
    pass


@profile_bp.post('/settings/update_credentials')
def update_credentials():
    user_id = session.get('id')

    # Fetch user from database
    user = UserTable.query.get(user_id)

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login_page'))

    try:
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        new_password = request.form.get('password')
        private_setting = request.form.get('private') == 'on'
        
        changes_made = False

        if new_email and new_email != '':
            user.email = new_email
            changes_made = True

        if new_phone and new_phone != '':
            user.phone = new_phone
            changes_made = True

        if new_password and new_password != '':
            hashed_password = bcrypt.generate_password_hash(new_password, 16).decode()
            user.password = hashed_password
            changes_made = True

        if user.private != private_setting:
            user.private = private_setting
            changes_made = True

        if changes_made:
            db.session.commit()
            flash('Credentials updated successfully', 'success')
        else:
            flash('No changes detected', 'error')

        return redirect(url_for('settings_page'))

    except Exception as e:
        flash(f'Unable to update credentials: {e}', 'error')
        return redirect(url_for('profile_bp.settings_page'))