from flask import session, url_for
from app import app


def test_access_session(client):
    response = client.post("/login", data={"username": "123", 
                            'password':'123'}, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert 'TRENDING' in data

def test_upload_video(client):
    with client.session_transaction() as session:
        session['id'] = 1
        response = client.post('/upload/new', data={
                'file':'example.mp4',
                'title':'example vid',
                'description':'sample desc'
        }, follow_redirects=True)
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'sample desc' in data