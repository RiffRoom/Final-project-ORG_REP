import pytest
from app import app
from models import UserTable, clear_data, db, JamSession, Party
from datetime import datetime
def test_sessions_and_party():
    #start by clearing the database
    clear_data()
    #assert users and jamsession is empty
    assert len(list(UserTable.query.all())) == 0
    assert len(list(JamSession.query.all())) == 0

    #create a new user - id 1
    newuser1 = UserTable('obamna', 'soda',
                        'The Barock', '123',
                        '44@gmail.com',
                        '123-456-7890')
    #add the new user
    db.session.add(newuser1)
    #commit
    db.session.commit()

    #create a new user - id2
    newuser2 = UserTable('Crazy', 'guy',
                        'Crazy guy', '123',
                        'ex@gmail.com',
                        '123-456-1230')
    db.session.add(newuser2)
    db.session.commit()

    #assert 2 users have been created and that they are in
    #the database
    assert len(list(UserTable.query.all())) == 2
    users = list(UserTable.query.all())
    assert 'Crazy guy' in str(users)
    assert 'obamna soda' in str(users)

    #create a jam session - has the id of 1
    sesh = JamSession('ex sesh', 'come on down', datetime.now(), datetime.now(),
                      10.000, 10.000, newuser1.id)
    db.session.add(sesh)
    db.session.commit()

    #assert there is 1 session now
    assert len(list(JamSession.query.all())) == 1
    #assert ex sesh is in the jamsession table
    assert 'ex sesh' in str(JamSession.query.all())
    

    #add user with id 2 into the party table for jamsession 1
    p = Party(sesh.id, newuser2.id)
    db.session.add(p)
    db.session.commit()

    #assert there is 1 record in the party table
    assert len(list(Party.query.all())) == 1
    #assert the row sesh exists is in the table
    assert f'{sesh.id}, {newuser2.id}' in str(Party.query.all())

    #the party p has been cancelled and will be removed from the jamsession table
    db.session.delete(sesh)
    db.session.commit()
    #assert there are no sessions or parties in their tables
    assert len(list(JamSession.query.all())) == 0
    assert len(list(Party.query.all())) == 0

    db.session.delete(newuser2)
    db.session.commit()
    db.session.delete(newuser1)
    db.session.commit()