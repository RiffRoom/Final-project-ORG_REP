from flask import Blueprint, render_template, redirect, url_for, request, abort, session, flash
from dotenv import load_dotenv
import os
from datetime import datetime
from models import UserTable, db, JamSession, Party

load_dotenv()

jam_sessions_bp = Blueprint('jam_sessions', __name__, template_folder='templates')


@jam_sessions_bp.get('/')
def get_sessions():
    if not session.get('id'):
        return redirect('/login')

    MAPS_API_KEY = os.getenv('MAPS_API_KEY')
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    max_date = datetime(2024, 12, 31,23)
    active_jam_sessions = JamSession.query.all()

    jam_session_data = []

    if active_jam_sessions:
        for i in active_jam_sessions:
            result = i.serialize
            date_str = JamSession.date_str(result['date'])
            jam_session_data.append(result)


    return render_template('jam_sessions.html', 
                        current_date=current_date, 
                        max_date=max_date, 
                        active_jam_sessions=active_jam_sessions,
                        jam_session_data=jam_session_data,
                        date_str=date_str, 
                        MAPS_API_KEY=MAPS_API_KEY,
                        jam_session=JamSession,
                        party=Party,
                        user_table=UserTable)



@jam_sessions_bp.post('/')
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

    s = JamSession(title, message, date, date_posted, lat, lng, session.get('id'))
    
    db.session.add(s)
    db.session.commit()

    p = Party(s.id, session.get('id'))
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('jam_sessions.get_sessions'))

@jam_sessions_bp.get('/<int:session_id>')
def get_single_session(session_id: int):
    jam_session = JamSession.query.get(session_id)
    return render_template('single_session.html', jam_session=jam_session)

@jam_sessions_bp.post('/<int:session_id>/delete')
def delete_session(session_id: int):
    session = JamSession.query.get(session_id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('jam_sessions.get_sessions'))

@jam_sessions_bp.post('<int:session_id>/join')
def join_session(session_id: int):
    jam_session = JamSession.query.get(session_id)
    party = Party.query.filter_by(session_id=jam_session.id, user_id=session.get('id')).first()
    if not party:
        party = Party(jam_session.id, session.get('id'))
        db.session.add(party)
        db.session.commit()
        flash(f'Joined {jam_session.host_name}s Session!')
        return redirect(url_for('jam_sessions.get_sessions'))
    else:
        flash('You are already in this session!')
        return redirect(url_for('jam_sessions.get_sessions'))

@jam_sessions_bp.post('<int:session_id>/leave')
def leave_session(session_id: int):
    jam_session = JamSession.query.get(session_id)
    party = Party.query.filter_by(session_id=jam_session.id, user_id=session.get('id')).first()
    if party:
        db.session.delete(party)
        db.session.commit()
        return redirect(url_for('jam_sessions.get_sessions'))
    else:
        return redirect(url_for('jam_sessions.get_sessions'))