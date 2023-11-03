from flask import Flask, render_template, redirect, url_for, request, abort
from models import db, Session
from dotenv import load_dotenv
import os


# Load environment variables

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')



app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.get('/sessions')
def get_sessions():
    active_sessions = Session.query.all()
    return render_template('sessions.html', active_sessions=active_sessions)


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


@app.route('/upload')
def uplaod_page():
    return None #rendertemplate('upload')