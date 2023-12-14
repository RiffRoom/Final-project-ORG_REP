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


@profile_bp.get('/')
def get_profile():
    user_id = session.get('id')
    user = UserTable.query.get(user_id)

    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    flask_env = current_app.config['FLASK_ENV']

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    
    flask_env = current_app.config['FLASK_ENV']
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    flask_env = current_app.config['FLASK_ENV']

    if flask_env == 'prod':
        return render_template('user_prof.html', user=user, user_posts=user_posts, is_own_profile=True, can_edit=True, distribution_url=distribution_url, flask_env=flask_env) 
    else:
        return render_template('user_prof.html', user=user, user_posts=user_posts, is_own_profile=True, can_edit=True, distribution_url='', flask_env=flask_env)

@profile_bp.get('/settings')
def get_settings():
    if not session.get('id'):
        return redirect('/login')

    current_user = UserTable.query.get(session.get('id'))
    if not current_user:
        flash('User not found.', 'error')
        return redirect('/login')

    current_user = UserTable.query.get(session.get('id'))
    private_setting = current_user.private

    if current_app.config['FLASK_ENV'] == 'prod':
        pfp = bucket_wrapper.get_object(s3_client, f'{current_app.config["PFP_PATH"]}testpfp.png')
        pfps = bucket_wrapper.get_objects(s3_client) 
        print(pfps)
        print(f'{distribution_url}{pfps[0]}/images/pfp/testpfp.png')
    else:
        pass
    return render_template('settings.html',user=current_user, private_setting=private_setting)

# To view another users profile
@profile_bp.get('/<int:user_id>')
def view_profile(user_id: int):
    current_user_id = session.get('id')
    user = UserTable.query.get(user_id)

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    is_private = user.private and current_user_id != user.id  
    is_own_profile = current_user_id == user.id
    can_edit = is_own_profile
    flask_env = current_app.config['FLASK_ENV']

    if current_app.config['FLASK_ENV'] == 'prod':
        return render_template('user_prof.html', user=user, user_posts=user_posts,  is_private=is_private, is_own_profile=is_own_profile, can_edit=can_edit, distribution_url=distribution_url, flask_env=flask_env) 
    else:
        return render_template('user_prof.html', user=user, user_posts=user_posts,  is_private=is_private, is_own_profile=is_own_profile, can_edit=can_edit, distribution_url='', flask_env=flask_env)

    


@profile_bp.route('/update_credentials', methods=['POST'])
def update_credentials():
    user_id = session.get('id')

    # Fetch user from database
    user = UserTable.query.get(user_id)

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login_page'))

    try:
        new_first_name = request.form.get('first_name')
        new_last_name = request.form.get('last_name')
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        new_bio = request.form.get('bio')
        private_setting = request.form.get('private') == 'on'
        
        changes_made = False

        if new_first_name and new_first_name != user.first_name:
            user.first_name = new_first_name
            changes_made = True

        if new_last_name and new_last_name != user.last_name:
            user.last_name = new_last_name
            changes_made = True

        if new_email and new_email != '':
            user.email = new_email
            changes_made = True

        if new_phone and new_phone != '':
            user.phone = new_phone
            changes_made = True

        if new_bio is not None:
            user.bio = new_bio
        else:
            user.bio = ''
            
        if user.private != private_setting:
            user.private = private_setting
            changes_made = True

        if changes_made:
            db.session.commit()
            flash('Credentials updated successfully', 'success')
        else:
            flash('No changes detected', 'error')

        return redirect(url_for('profiles.get_profile', username=user.user_name))

    except Exception as e:
        flash(f'Unable to update credentials: {e}', 'error')
        return redirect(url_for('profiles.get_settings'))


@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    user_id = session.get('id')
    user = UserTable.query.get(user_id)

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login_page'))

    try:
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')

        if current_password and new_password:
            if bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash('Password updated successfully.', 'success')
            else:
                flash('Current password is incorrect.', 'error')
        else:
            flash('Please provide both current and new password.', 'error')

        return redirect(url_for('profiles.get_settings'))


    except Exception as e:
        flash(f'Error changing password: {e}', 'error')
        return redirect(url_for('profiles.get_settings'))


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

@profile_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    user_id = session.get('id')
    post = Post.query.get(post_id)

    if not post or post.user_id != user_id:
        flash('Post not found or access denied', 'error')
        return redirect(url_for('profiles.get_profile'))

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('profiles.get_profile'))
