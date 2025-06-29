from . import db
from flask_login import UserMixin
from sqlalchemy import func, Table
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, BINARY
from sqlalchemy.orm import declarative_base, relationship


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password =  db.Column(db.String(100))
    full_name = db.Column(db.String(100))

    user_playlists = db.relationship('Playlist', back_populates='user', cascade='all, delete-orphan')

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password =  db.Column(db.String(100))


class Creator(db.Model, UserMixin):
    __tablename__ = 'creator'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password =  db.Column(db.String(100))

    creator_playlists = db.relationship('Playlist', back_populates='creator', cascade='all, delete-orphan')


class Album(db.Model, UserMixin):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    genre = Column(String)
    artist = Column(String, nullable=False)
    date_created = Column(Integer)
    flag = db.Column(db.Boolean, default=False)
    songs = relationship('Song', back_populates='album')

song_playlist_association = db.Table(
    'song_playlist_association',
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'))
)

class Song(db.Model, UserMixin):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    artist = Column(Text)
    Genre = Column(Text)
    duration = Column(Integer)
    date_created = Column(Integer)
    lyrics = Column(Text)
    file = Column(Text)
    flag = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0)
    ratings = db.relationship('Rating', backref='song', lazy=True)

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album', back_populates='songs')
    playlists = db.relationship('Playlist', secondary=song_playlist_association, back_populates='songs')

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='user_playlists')

    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    creator = db.relationship('Creator', back_populates='creator_playlists')

    # Define many-to-many relationship with Song
    songs = db.relationship('Song', secondary=song_playlist_association, back_populates='playlists')

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)


class Blacklist(db.Model, UserMixin):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password =  db.Column(db.String(100))