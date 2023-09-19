from app import db
from flask_login import UserMixin

#user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashing should be applied
    favorites = db.relationship('Club', secondary='favorites', backref='users')

#club table
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    tags = db.relationship('Tag', secondary='club_tags', backref='clubs')

#tag table
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
#file table
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_code = db.Column(db.String(50), db.ForeignKey('club.code'), nullable=False)
    filename = db.Column(db.String(255), unique = True, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(255), nullable=False)

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True)
)

club_tags = db.Table('club_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True)
)
