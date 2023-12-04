import pytest
from app import app
from models import UserTable, clear_bd, db

@pytest.fixture()
def test_app():
    return app.test_client()

def test_ex():
    assert 1 == 1

# def test_new_signup(test_app):
#     #clearing the database
#     clear_bd()
#     assert db.all() is None

#     newuser = UserTable('obamna', 'soda',
#                         'The Barock', '123',
#                         '44@gmail.com', False,
#                         '123-456-7890', None)
#     db.add(newuser)
#     db.commit()
#     assert 1 != 2
    

