import pytest
from app import app, bcrypt, upload_bp, profile_bp, jam_sessions_bp
import models
from blueprints.uploader.upload import get_upload_page, upload_video

# def create_test_user():
#         passw = bcrypt.generate_password_hash('123', 16).decode()
#         test_user = models.UserTable('test', 'user', '123', passw, 'test@email.com', 34232342345)
#         models.db.session.add(test_user)
#         models.db.session.commit()
#         return None

@pytest.fixture(scope='function')
def client():
    passw = bcrypt.generate_password_hash('123', 16).decode()
    test_user = models.UserTable('test', 'user', '123', passw, 'test@email.com', 34232342345)
    models.db.session.add(test_user)
    models.db.session.commit()
    with app.test_client() as client:
        yield client
        models.db.session.delete(test_user)
        models.db.session.commit()

def t_login():
    client.post('/login', data={
        'username':'123',
        'password':'123'}, follow_redirects=True)
    
def t_logout():
    client.post('/logout')

@pytest.fixture(scope='module')
def test_app():
    passw = bcrypt.generate_password_hash('123', 16).decode()
    test_user = models.UserTable('test', 'user', '123', passw, 'test@email.com', 34232342345)
    models.db.session.add(test_user)
    models.db.session.commit()
    with app.test_client() as client:
        yield client
        models.db.session.delete(test_user)
        models.db.session.commit()