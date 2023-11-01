from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'mock_data'
    session_id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    user_name = db.Column("username" ,db.String(50), unique=True, nullable=False)
    message = db.Column("message", db.String(50), nullable=False)
    date = db.Column("date", db.DateTime, nullable=False)
    lat = db.Column("latitude", db.Double, nullable=False)
    lng = db.Column("longitude", db.Double, nullable=False)