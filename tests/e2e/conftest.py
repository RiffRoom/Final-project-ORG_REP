import pytest
from app import app
import models
from blueprints.uploader.upload import get_upload_page, upload_video

# def create_test_user():
#         test_user = models.UserTable('test', 'user', '123', '123', 'test@email.com', 34232342345)
#         models.db.session.add(test_user)
#         models.db.session.commit()
#         return None

@pytest.fixture(scope='module')
def test_app():
    with app.test_client() as client:
        yield client
