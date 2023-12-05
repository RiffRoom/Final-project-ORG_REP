import pytest
from app import app
from models import UserTable, clear_bd, db, clear_data

def test_ex():
    assert 1 == 1

def test_new_signup():
    #clearing the database
    clear_data()
    # asserting database is clear
    assert len(list(UserTable.query.all())) is 0

    newuser = UserTable('obamna', 'soda',
                        'The Barock', '123',
                        '44@gmail.com',
                        '123-456-7890')
    db.session.add(newuser)
    db.session.commit()


    Users = list(UserTable.query.all())
    assert len(list(UserTable.query.all())) == 1
    newuser = UserTable('Crazy', 'guy',
                        'Crazy guy', '123',
                        'ex@gmail.com',
                        '123-456-1230')
    db.session.add(newuser)
    Users = list(UserTable.query.all())
    assert 'Crazy guy' not in Users
    db.session.commit()
    Users = UserTable.query.all()
    assert 'Crazy guy' in str(Users)
    

