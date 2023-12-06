import pytest
from app import app
from models import UserTable, clear_data, db

def test_new_signup():
    #clearing the database
    clear_data()
    # asserting database is clear or has a length of 0
    assert len(list(UserTable.query.all())) is 0
    #create a new user
    newuser = UserTable('obamna', 'soda',
                        'The Barock', '123',
                        '44@gmail.com',
                        '123-456-7890')
    #add the new user
    db.session.add(newuser)
    #commit
    db.session.commit()


    Users = list(UserTable.query.all())
    #assert that a new user is added, length of 1
    assert len(list(UserTable.query.all())) == 1
    newuser = UserTable('Crazy', 'guy',
                        'Crazy guy', '123',
                        'ex@gmail.com',
                        '123-456-1230')
    db.session.add(newuser)
    Users = list(UserTable.query.all())
    db.session.commit()
    #test after session commit
    Users = UserTable.query.all()
    assert 'Crazy guy' in str(Users)
    

