from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/sesh')
def sesh_page():
    return render_template('sessions.html')

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