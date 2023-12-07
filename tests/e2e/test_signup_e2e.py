from app import app

def test_reach_signup(test_app):
    respone = test_app.get('/login')
    data = respone.data.decode('utf-8')
    assert respone.status_code == 200
    assert 'Riff Room' in data
    assert 'Login' in data
    assert 'Username' in data
    assert 'Password' in data
    assert 'Forgot Password?' in data
    assert 'New to RiffRoom? <a href="#" class="text-decoration-none">Create an Account' in data

def test_live_signup(test_app):
    response = test_app.post('/signup', data={
        'first_name':'Jack',
        'last_name':'Snipes',
        'email':'JS@gm.com',
        'phone':'123-123-1230',
        'username':'JackySnips',
        'raw_password':'123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_live_login(test_app):
    response = test_app.post('/login', data={
        'username':'JackySnips',
        'raw_password':'123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_bad_signup(test_app):
    response = test_app.post('/signup', data={
        'first_name':'Jack',
        'last_name':'Snipes',
        'email':'JS@gm.com',
        'phone':'123-123-1230',
        'username':None,
        'raw_password':''
    }, follow_redirects=False)
    assert response.status_code == 302

def test_bad_login(test_app):
    response = test_app.post('/login', data={
        'username':'JackySnip',
        'raw_password':'12'
    }, follow_redirects=False)
    assert response.status_code == 302

    response = test_app.post('/login', data={
        'username':'asdasdasdasd',
        'raw_password':'asdasdasdasd'
    }, follow_redirects=False)
    assert response.status_code == 302