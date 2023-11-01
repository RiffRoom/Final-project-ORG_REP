from flask import Flask, render_template, redirect, url_for, request, abort

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
    return None #rendertemplate('settings.html')

@app.route('/upload')
def uplaod_page():
    return None #rendertemplate('upload')