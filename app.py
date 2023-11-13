from flask import Flask, render_template, redirect, url_for, request, abort, jsonify
from models import db, Session, UserTable, Comment, CommentSection, Post, Party, insert_BLOB_user, return_media, return_img, insert_BLOB_post
from dotenv import load_dotenv
import os
import base64
from datetime import datetime, timedelta


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
    return render_template('index.html', users=db.session.query(Post).all())

#note binary_corrector is ONLY for profile pics and takes in
#a authentic UserTable id!!
@app.context_processor
def db_image_corrector():
    return dict(binary_corrector=return_img) 
## using context_processor for images
# loop example! start with a for loop in jinja
# {% for user in users%} 
#           then call {{binary_corrector()}} leave the user id as is
#                                         like this  vvvv    thats it
#         <img src="data:;base64,{{binary_corrector(user.id)}}">
#     {% endfor %} 


#db_media corrector is ONLY for audio and videos for posts and takes in
# a Post Table id!!
@app.context_processor
def db_media_corrector():
    return dict(media_binary_corrector=return_media)
# example for audio!
# {% for user in users%} 
#     <audio controls>
#         <source src="data:;base64,{{media_binary_corrector(2)}}" type="audio/mpeg">
#     </audio>  
# {% endfor %} 

#FUN FACT! you can get away with saying video for audio,
#with this you can kill 2 birds with 1 stone but must specify the type!
# {% for user in users%} 
#     <video controls>
#         <source src="data:;base64,{{media_binary_corrector(user.id)}}" type="audio/mpeg">
#     </video>  
# {% endfor %} 


#examples for working with post and user profile pic
# insert_BLOB_user(2, 'static\images\logo.png')
# insert_BLOB_user(3, 'static\images\pfp.png')

# pos1 = Post('Shape of my Heart Cover', 'I made a cover of a favorite song of mine, check it out!',
#             0, datetime.now(), 3, 'static\samplevids\Recording.mp3')
# db.session.add(pos1)
# db.session.commit()

# insert_BLOB_post(1, 'static\samplevids\Recording.mp3')


@app.get('/sessions')
def get_sessions():
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_sessions = Session.query.all()

    session_data = []

    for i in active_sessions:
        result = i.serialize
        date_str = Session.date_str(result['date'])
        session_data.append(result)
        
        

    return render_template('sessions.html', current_date=current_date, max_date=max_date, active_sessions=active_sessions, session_data=session_data, date_str=date_str)

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

@app.route('/set_test_profile_pic', methods=['POST'])
def set_test_profile_pic():
    test_pic_web_path = '/static/images/testpfp.png'
    return jsonify({'new_pic_path': test_pic_web_path})
    
@app.route('/upload')
def uplaod_page():
    return None #rendertemplate('upload')