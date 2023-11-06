from flask import Flask, render_template, redirect, url_for, request, abort
from models import db, Session, UserTable
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
    return render_template('index.html')

@app.get('/sessions')
def get_sessions():
    active_sessions = Session.query.all()

    # us = UserTable('Nail', 'Claros', 'ncdash', 'pswd', 'nc@gmail.com', 68968942) ## id 3
    # db.session.add(us)
    # db.session.commit()

    #base logic, id must exsist already
    # s = Session('Sample Title-2', 'YYYYYYAAA-2', '2023-10-01', 34.121212121313, 35.21324232323232, 3)
    # db.session.add(s)
    # db.session.commit()

    # concept for alternate session instantiation
    # s = sessions.full('Dve Char', 'samp 2', 'smap msggg', '2023-10-01', 34.12121221212, 35,14122323221312, 5)
    # db.session.add(s)
    # db.session.commit()
    return render_template('sessions.html', active_sessions=active_sessions)


@app.get('/sessions/<int:session_id>')
def get_single_session(session_id: int):
    session = Session.query.get(session_id)
    return render_template('get_single_session.html', session=session)


@app.get('/sessions/new_session')
def get_new_sessions_form_page():
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    return render_template('new_session.html', current_date=current_date, max_date=max_date)

@app.post('/sessions/new_session')
def add_new_session():
    data = request.get_json()
    print(data)
    title = data['title']
    message = data['message']
    lat = data['lat']
    lng = data['lng']
    date = data['date']
    s = Session(title, message, date, lat, lng, 1)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('get_sessions'))


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