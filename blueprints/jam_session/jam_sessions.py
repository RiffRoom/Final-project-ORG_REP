from flask import Blueprint, flash, render_template, redirect, url_for, request, abort, jsonify, session
from dotenv import load_dotenv
import os
from datetime import datetime
from models import db, JamSession

load_dotenv()

jam_sessions_bp = Blueprint('jam_sessions', __name__, template_folder='templates')


@jam_sessions_bp.get('/')
def get_sessions():
    if not session.get('id'):
        return redirect('/login')

    MAPS_API_KEY = 'AIzaSyBB9K1RjPnWTNAvCWp5xkrCjT5o5xpx2Bo'
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_jam_sessions = JamSession.query.all()

    jam_session_data = []

    for i in active_jam_sessions:
        result = i.serialize
        date_str = JamSession.date_str(result['date'])
        jam_session_data.append(result)

    return render_template('jam_sessions.html', current_date=current_date, max_date=max_date, active_jam_sessions=active_jam_sessions, jam_session_data=jam_session_data, date_str=date_str, MAPS_API_KEY=MAPS_API_KEY)



@jam_sessions_bp.post('/new')
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

    s = JamSession(title, message, date, date_posted, lat, lng, 1)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('get_sessions'))

@jam_sessions_bp.get('/<int:session_id>')
def get_single_session(session_id: int):
    session = JamSession.query.get(session_id)
    return render_template('get_single_session.html', session=session)

@jam_sessions_bp.post('/<int:jam_session_id>/delete')
def delete_session(session_id: int):
    session = JamSession.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('get_sessions'))
