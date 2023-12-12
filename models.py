from flask_sqlalchemy import SQLAlchemy
import contextlib
import base64
from datetime import datetime

def convert_To_Binary(filename): 
    with open(filename, 'rb') as file: 
        data = file.read() 
    return data 

def return_img(id):
    some_user = UserTable.query.get(id)
    BLOB = some_user.prof_pic
    image = base64.b64encode(BLOB).decode('ascii')
    return image

##update a user profile pic
def insert_BLOB_user(user_id, FileName): 
    """ insert a BLOB into a table """
    user = UserTable.query.get(user_id)
    user.prof_pic = convert_To_Binary(FileName)
    db.session.commit()

##update a post's file
def insert_BLOB_post(user_id, FileName): 
    """ insert a BLOB into a table """
    user = Post.query.get(user_id)
    user.post_file = convert_To_Binary(FileName)
    db.session.commit()

def return_media(id):
    some_user = Post.query.get(id)
    BLOB = some_user.post_file
    image = base64.b64encode(BLOB).decode('ascii')
    return image


def get_comments_of_post(id):
    comment_section = CommentSection.query.filter_by(post_id=id).first()
    comments = list(Comment.query.filter_by(comment_section_id=comment_section.id).all())
    return comments

def time_since_post(pid):
    postex = Post.query.get(pid)
    delta = datetime.now() - postex.date_posted
    secs = delta.total_seconds()
    if secs < 60.00:
        return f'uploaded %.0f seconds ago' % secs
    
    if secs >= 60.00 and secs < (60*60):
        secs = (secs / (60))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f minute ago' % secs
        else:
            return f'uploaded %.0f minutes ago' % secs
        
    if secs >= (60*60) and secs <= (60*60*24):
        secs = (secs / (60*60))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f hour ago' % secs
        else:
            return f'uploaded %.0f hours ago' % secs
        
    if secs >= (60*60*24) and secs <= (60*60*24*7):
        secs = (secs / (60*60*24))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f day ago' % secs
        else:
            return f'uploaded %.0f days ago' % secs

    if secs >= (60*60*24*7) and secs < (60*60*24*7*4):
        secs = (secs / (60*60*24*7))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f week ago' % secs
        else:
            return f'uploaded %.0f weeks ago' % secs

    if secs >= (60*60*24*7*4) and secs < (60*60*24*7*4*12):
        secs = (secs / (60*60*24*7*4))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f month ago' % secs
        else:
            return f'uploaded %.0f months ago' % secs
        
    if secs >= (60*60*24*7*4*12):
        secs = (secs / (60*60*24*7*4*12))
        if f'%.0f'%secs == '1':
            return f'uploaded %.0f year ago' % secs
        else:
            return f'uploaded %.0f years ago' % secs
        
    return None

def time_since_jam_session(jam_session_id):
    jam_session = JamSession.query.get(jam_session_id)
    delta = datetime.now() - jam_session.date_posted
    secs = delta.total_seconds()
    if secs < 60.00:
        return f'%.0f seconds ago' % secs
    
    if secs >= 60.00 and secs < (60*60):
        secs = (secs / (60))
        if f'%.0f'%secs == '1':
            return f'%.0f minute ago' % secs
        else:
            return f'%.0f minutes ago' % secs
        
    if secs >= (60*60) and secs <= (60*60*24):
        secs = (secs / (60*60))
        if f'%.0f'%secs == '1':
            return f'%.0f hour ago' % secs
        else:
            return f'%.0f hours ago' % secs
        
    if secs >= (60*60*24) and secs <= (60*60*24*7):
        secs = (secs / (60*60*24))
        if f'%.0f'%secs == '1':
            return f'%.0f day ago' % secs
        else:
            return f'%.0f days ago' % secs

    if secs >= (60*60*24*7) and secs < (60*60*24*7*4):
        secs = (secs / (60*60*24*7))
        if f'%.0f'%secs == '1':
            return f'%.0f week ago' % secs
        else:
            return f'%.0f weeks ago' % secs

    if secs >= (60*60*24*7*4) and secs < (60*60*24*7*4*12):
        secs = (secs / (60*60*24*7*4))
        if f'%.0f'%secs == '1':
            return f'%.0f month ago' % secs
        else:
            return f'%.0f months ago' % secs
        
    if secs >= (60*60*24*7*4*12):
        secs = (secs / (60*60*24*7*4*12))
        if f'%.0f'%secs == '1':
            return f'%.0f year ago' % secs
        else:
            return f'%.0f years ago' % secs
        
    return None


db = SQLAlchemy()
# USE ONLY FOR TESTS
def clear_bd():
    meta = db.metadata( )
    for table in reversed(meta.sorted_tables):
        print("Clear table %s" % table) 
        db.execute(table.delete())
    db.commit()


class UserTable(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    private = db.Column(db.Boolean, nullable=True, default=False)
    phone = db.Column(db.String(20), nullable=True)
    prof_pic = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    

    def __init__(self, first_n: str, last_n: str, user_n: str, pswd: str, email: str, phone: int, bio: str = None) -> None:
        self.first_name = first_n
        self.last_name = last_n
        self.user_name = user_n
        self.password = pswd
        self.email = email
        self.phone = phone
        self.bio = bio 
    
    def return_img(BLOB, file):
        with open(f"{file}", 'wb') as file: 
            file.write(BLOB) 
        return file

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
class JamSession(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    host_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    lat = db.Column( db.Double, nullable=False)
    long = db.Column(db.Double, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    party = db.relationship('Party', cascade="all, delete")

    
    ## create instance without host_name and just id
    def __init__(self, title: str, msg: str, date: date, date_p: date, lat: float, long: float, h_id: int) -> None:
        self.host_name = JamSession.get_user_name_id(h_id)
        self.title = title
        self.message = msg
        self.date = date
        self.date_posted = date_p
        self.lat = lat
        self.long = long
        self.host_id = h_id
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'host_name': self.host_name,
            'title': self.title,
            'message': self.message,
            'date': self.date,
            'date_posted': self.date_posted,
            'lat': self.lat,
            'lng': self.long
        }
    
    def get_user_name_id(a: int):
        s = db.session()
        return s.query(UserTable).filter(UserTable.id == a).first().first_name + ' ' + s.query(UserTable).filter(UserTable.id == a).first().last_name

    def date_str(date: datetime):
        return date.strftime('%A %b, %d  %I:%M %p')
    
    def get_num_attendees(id: int):
        jam_session = JamSession.query.get(id)
        num_attendees = Party.query.filter_by(session_id=jam_session.id).count()
        return num_attendees

#class party
class Party(db.Model):
    __tablename__ = 'party'
    party_id = db.Column(db.Integer, primary_key=True, nullable= False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)

    def __init__(self, sesh_id: int, user_id: int) -> None:
        self.session_id = sesh_id
        self.user_id = user_id

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    msg = db.Column(db.String(255), nullable=True)
    ratio = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    section = db.relationship('CommentSection', cascade='all, delete')

    def __init__(self, video_id:str, title: str, msg: str, ratio: int, date: datetime, user_id: int) -> None:
        self.video_id = video_id
        self.title = title
        self.msg = msg
        self.ratio = ratio
        self.date_posted = date
        self.user_id = user_id


class CommentSection(db.Model):
    __tablename__ = 'comment_section'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comments = db.relationship('Comment', cascade="all, delete")
    def __init__(self, post_id: int) -> None:
        self.post_id = post_id

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    comment_section_id = db.Column(db.Integer, db.ForeignKey('comment_section.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __init__(self, cs_id: int, user_id: int, msg: str) -> None:
        self.comment_section_id = cs_id
        self.user_id = user_id
        self.message = msg