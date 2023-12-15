import pytest
from app import app
from models import UserTable, clear_data, db

def test_new_signup():
    #clearing the database
    clear_data()
    # asserting database is clear or has a length of 0
    assert len(list(UserTable.query.all())) is 0
    #create a new user
    newuser1 = UserTable('obamna', 'soda',
                        'The Barock', '123',
                        '44@gmail.com',
                        '123-456-7890')
    #add the new user
    db.session.add(newuser1)
    #commit
    db.session.commit()

    #assert that a new user is added, length of 1
    assert len(list(UserTable.query.all())) == 1
    newuser2 = UserTable('Crazy', 'guy',
                        'Crazy guy', '123',
                        'ex@gmail.com',
                        '123-456-1230')
    db.session.add(newuser2)
    db.session.commit()
    #assert the length of usertable is now 2
    assert len(list(UserTable.query.all())) == 2
    #test after session commit
    assert 'Crazy guy' in str(UserTable.query.all())
    
    #newuser 2 decides to leave the platform
    #remove user2
    db.session.delete(newuser2)
    db.session.commit()
    #assert there is only one use in the usertable
    assert len(list(UserTable.query.all())) == 1
    #and assert no user exsists as crazy guy
    assert 'Crazy guy' not in str(UserTable.query.all())

    db.session.delete(newuser1)
    db.session.commit()