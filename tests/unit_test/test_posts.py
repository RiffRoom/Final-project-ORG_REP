import pytest
from app import app
from models import UserTable, clear_data, db, Post, CommentSection, Comment
from datetime import datetime

def test_posts():
    #start with clearing the database
    clear_data()
    #assert all relavent database tables are empty
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
    #add 
    db.session.add(newuser2)
    #commit
    db.session.commit()

    #assert 2 users have been created and that they are in
    #the database
    assert len(list(UserTable.query.all())) == 2
    users = list(UserTable.query.all())
    assert 'Crazy guy' in str(users)
    assert 'obamna soda' in str(users)

    #create a new post with comment section
    p = Post('fake_id', 'Example Post', 'example descriptions', 0, datetime.now(), newuser1.id)
    db.session.add(p)
    db.session.commit()
    p_comsec = CommentSection(p.id)
    db.session.add(p_comsec)
    db.session.commit()

    #assert that post table has one entry and that entry contains the title and user id
    assert len(list(Post.query.all())) == 1
    assert f'{newuser1.id}, Example Post' in str(Post.query.all())
    #assert that comment section has been created for the p Post
    assert len(list(CommentSection.query.all())) == 1
    assert f'{p_comsec.id}, {p.id}' in str(CommentSection.query.all())
    #the comments table should still be empty as we have a section but no comments yet
    assert len(list(Comment.query.all())) == 0

    #newuser 2 creates a comment in the comment section p Post
    comment = Comment(p_comsec.id, newuser2.id, 'Cool')
    db.session.add(comment)
    db.session.commit()

    #assert this comment has been added
    assert len(list(Comment.query.all())) == 1
    assert f'{p_comsec.id}, {newuser2.id}, Cool' in str(Comment.query.all())

    #newuser2 regrets his comment and removes it
    db.session.delete(comment)
    db.session.commit
    #assert the comments table is empty
    assert len(list(Comment.query.all())) == 0
    assert f'{p_comsec.id}, {newuser2.id}, Cool' not in str(Comment.query.all())

    #newuser1 didnt like his post and decides to remove it
    db.session.delete(p)
    db.session.commit()

    #assert the post and comment section table are empty
    assert len(list(Post.query.all())) == 0
    assert len(list(CommentSection.query.all())) == 0