from flask_sqlalchemy import SQLAlchemy
import psycopg2
import config
from datetime import datetime

def convert_To_Binary(filename): 
    with open(filename, 'rb') as file: 
        data = file.read() 
    return data 

def insert_BLOB(S_No, FileName): 
    """ insert a BLOB into a table """
    conn = None
    try: 

        # connect to the PostgreSQL server & creating a cursor object 
        conn = psycopg2.connect(**config) 

        # Creating a cursor with name cur. 
        cur = conn.cursor() 

        # Binary Data 
        file_data = convert_To_Binary(FileName) 

        # BLOB DataType 
        BLOB = psycopg2.Binary(file_data) 

        # SQL query to insert data into the database. 
        cur.execute( 
            "INSERT INTO blob_datastore(s_no,file_name,blob_data) VALUES(%s,%s,%s)", (S_No, FileName, BLOB)) 

        # Close the connection 
        cur.close() 

    except(Exception, psycopg2.DatabaseError) as error: 
        print(error) 
    finally: 
        if conn is not None: 
            # Commit the changes to the database 
            conn.commit() 


db = SQLAlchemy()
## USE ONLY FOR TESTS
# def clear_bd():
#     return None


class UserTable(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    private = db.Column(db.Boolean, nullable=True, default=False)
    phone = db.Column(db.Integer, nullable=False)
    profile_pic = db.Column(db.LargeBinary, nullable=False)
    

    def __init__(self, first_n: str, last_n: str, user_n: str, pswd: str, email: str, phone: int) -> None:
        self.first_name = first_n
        self.last_name = last_n
        self.user_name = user_n
        self.password = pswd
        self.email = email
        self.phone = phone

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    host_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    lat = db.Column( db.Double, nullable=False)
    long = db.Column(db.Double, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    party = db.relationship('Party', cascade="all, delete")

    
    ## create instance without host_name and just id
    def __init__(self, title: str, msg: str, date: date, lat: float, long: float, h_id: int) -> None:
        self.host_name = Session.get_user_name_id(h_id)
        self.title = title
        self.message = msg
        self.date = date
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
            'lat': self.lat,
            'lng': self.long
        }
    
    def get_user_name_id(a: int):
        s = db.session()
        return s.query(UserTable).filter(UserTable.id == a).first().first_name + ' ' + s.query(UserTable).filter(UserTable.id == a).first().last_name

    def date_str(date: datetime):
        return date.strftime('%A %b, %d  %I:%M %p')


#class party
class Party(db.Model):
    __tablename__ = 'party'
    party_id = db.Column(db.Integer, primary_key=True, nullable= False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)

    def __init__(self, sesh_id: int, u_id: int) -> None:
        self.session_id = sesh_id
        self.user_id = u_id
        self.user_name = Session.get_user_name_id(u_id)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    ratio = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    post_file = db.Column(db.LargeBinary, nullable=False)
    section = db.relationship('CommentSection', cascade='all, delete')

    def __init__(self, title: str, msg: str, ratio: int, date: str, pid: int) -> None:
        self.title = title
        self.description = msg
        self.ratio = ratio
        self.date_posted = date
        self.user_id = pid
        self.user_name = Session.get_user_name_id(pid)


class CommentSection(db.Model):
    __tablename__ = 'comment_section'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comments = db.relationship('Comment', cascade="all, delete")
    def __init__(self, post_id: int) -> None:
        self.post_id = post_id

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    comment_section_id = db.Column(db.Integer, db.ForeignKey('comment_section.id'), nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    commenter_name = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __init__(self, cs_id: int, cid: int, msg: str) -> None:
        self.comment_section_id = cs_id
        self.commenter_id = cid
        self.commenter_name = Session.get_user_name_id(cid)
        self.message = msg