

def test_upload_video(test_app):
    response = test_app.post('/login', data={
        'username':'123',
        'password':'123'
    }, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert 'TRENDING' in data

    response = test_app.post('/upload/new', data={
            'file':'example.mp4',
            'title':'example vid',
            'description':'sample desc'
    }, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'sample desc' in data