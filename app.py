
from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
from models import db, Session, UserTable, Comment, CommentSection, Post, Party, insert_BLOB

from dotenv import load_dotenv
import os
from datetime import datetime

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
    # insert_BLOB(1, 'static\images\default.png')
    return render_template('index.html', users=UserTable.query.all())

@app.get('/sessions')
def get_sessions():
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_sessions = Session.query.all()
    session_data = [i.serialize for i in active_sessions]
    return render_template('sessions.html', current_date=current_date, max_date=max_date, active_sessions=active_sessions, session_data=session_data)

@app.post('/sessions')
def add_new_session():
    data = request.get_json()
    title = data['title']

    if title is None or title == '':
        abort(400)

    message = data['message']

    lat = data['lat']
    lng = data['lng']
    print(lat, lng)

    if lat is None or lat == '' or lng is None or lng == '':
        abort(400)

    date = data['date']

    if date is None or date == '':
        abort(400)

    s = Session(title, message, date, lat, lng, 1)
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



@app.route('/upload')
def uplaod_page():
    return None #rendertemplate('upload')