import pytest
from app import app
from models import UserTable, clear_data, db, Post, CommentSection, Comment
from datetime import datetime

def test_posts():
    #start with clearing the database
    clear_data()
    assert len(list(UserTable.query.all())) == 0
    assert len(list(Post.query.all())) == 0
    assert len(list(CommentSection.query.all())) == 0
    assert len(list(Comment.query.all())) == 0
    
    #create a new user - newuser1
    newuser1 = UserTable('obamna', 'soda',
                        'The Barock', '123',
                        '44@gmail.com',
                        '123-456-7890')
    #add the new user
    db.session.add(newuser1)
    #commit
    db.session.commit()

    #create a new user - newuser2
    newuser2 = UserTable('Crazy', 'guy',
                        'Crazy guy', '123',
                        'ex@gmail.com',
                        '123-456-1230')
    db.session.add(newuser2)
    db.session.commit()