from operator import or_
from flask import Blueprint, render_template, request, flash, redirect, sessions, url_for
from sqlalchemy import create_engine
from .models import User, Admin, Creator, Song, Playlist, Blacklist, Album
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import login_user,login_required,logout_user, current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
import sqlite3




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if (user.password == password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.user_page'),)
            else:
                flash('Incorrect password! Try again...', category='error')
        else:
            flash('Email does not exist!', category='error')
    data= request.form
    return render_template("login.html")

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select

Base = declarative_base()

engine = create_engine('sqlite:///instance/database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@auth.route('/user_page', methods=['GET','POST'])
#@login_required
def user_page():
    # Fetch top-rated songs from the database
    top_songs = session.query(Song).order_by(Song.rating.desc()).limit(6).all()
    new_songs = session.query(Song).order_by(Song.date_created.asc()).limit(6).all()
    new_albums = session.query(Album).order_by(Album.date_created.asc()).limit(6).all()
    # Render the HTML page with the list of top-rated songs
    return render_template('user_page.html', songs =top_songs, new_songs=new_songs,new_albums=new_albums)


@auth.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists! Try to Log in...',category='error')
        elif len(email) <4:
            flash('Email is too short!',category='error')
        #elif len(full_name) <2:
            #flash('Name must greater than 2 characters!',category='error')
        elif password1 != password2:
            flash('Passwords do not match!',category='error')
        elif len(password1)<5:
            flash('Password is too short! Try with more than 4 characters!',category='error')
        else:
            #new_user= User(email=email, full_name=full_name, password=generate_password_hash(password1, method='sha256'))
            new_user= User(email=email, full_name=full_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)
            flash('Signed up Successfully! Redirecting to your User page...',category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('auth.user_page'))
    return render_template("signup.html")



@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if (admin.password == password):
                flash('Logged in successfully!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for('auth.admin_page'),)
            else:
                flash('Incorrect password! Try again...', category='error')
        else:
            flash('Admin does not exist!', category='error')
    data= request.form
    return render_template("admin_login.html")


from sqlalchemy import func, distinct
@auth.route('/admin_page', methods=['GET','POST'])
#@login_required
def admin_page():
    songs = Song.query.all()
    song_count = Song.query.count()
    user_count = User.query.count()
    whitelist_count = Creator.query.count()
    blacklist_count = Blacklist.query.count()
    creator_count = whitelist_count+blacklist_count
    album_count = Album.query.count()
    ave_ratings = session.query(func.avg(Rating.rating)).scalar()
    playlist_user = session.query(func.count(distinct(User.id))).\
    join(User.user_playlists).\
    scalar()
    rating_user = session.query(func.count(distinct(Rating.user_id))).scalar()
    # Extract JSON-serializable data from Song objects
    song_data = [{'title': song.name, 'rating': song.rating} for song in songs]

    return render_template("admin_page.html", songs=song_data,song_count=song_count,
                           creator_count=creator_count,blacklist_count=blacklist_count,whitelist_count=whitelist_count,
                           user_count=user_count, album_count=album_count,ave_ratings=ave_ratings,playlist_user=playlist_user,
                           rating_user=rating_user)

@auth.route('/creator_login', methods=['GET', 'POST'])
def creator_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        creator = Creator.query.filter_by(email=email).first()
        if creator:
            if (creator.password == password):
                flash('Logged in successfully!', category='success')
                login_user(creator, remember=True)
                return redirect(url_for('auth.creator_page'),)
            else:
                flash('Incorrect password! Try again...', category='error')
        else:
            flash('Creator does not exist!', category='error')
    data= request.form
    return render_template("creator_login.html")

@auth.route('/creator_page', methods=['GET','POST'])
#@login_required
def creator_page():
    # Fetch top-rated songs from the database
    top_songs = session.query(Song).order_by(Song.rating.desc()).limit(6).all()
    new_songs = session.query(Song).order_by(Song.date_created.asc()).limit(6).all()
    new_albums = session.query(Album).order_by(Album.date_created.asc()).limit(6).all()
    album_count = Album.query.count()
    song_count = Song.query.count()
    ave_ratings = session.query(func.avg(Rating.rating)).scalar()

    # Render the HTML page with the list of top-rated songs
    return render_template('creator_page.html', songs =top_songs, new_songs=new_songs,new_albums=new_albums,song_count=song_count, album_count=album_count,ave_ratings=ave_ratings)

@auth.route('/creator_signup', methods=['GET', 'POST'])
def creator_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        creator = Creator.query.filter_by(email=email).first()
        if creator:
            flash('Email already exists! Try to Log in...',category='error')
        elif len(email) <4:
            flash('Email is too short!',category='error')
        elif password1 != password2:
            flash('Passwords do not match!',category='error')
        elif len(password1)<5:
            flash('Password is too short! Try with more than 4 characters!',category='error')
        else:
            #new_user= User(email=email, full_name=full_name, password=generate_password_hash(password1, method='sha256'))
            new_creator= Creator(email=email, password=password1)
            db.session.add(new_creator)
            db.session.commit()
            #login_user(user, remember=True)
            flash('Signed up Successfully! Redirecting to your Creator page...',category='success')
            return redirect(url_for('auth.creator_page'))
    return render_template("signup.html")

from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, TextAreaField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired

class SongForm(FlaskForm):
    name = StringField('Song Name', validators=[DataRequired()])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
    duration = IntegerField('Duration (Minutes)', validators=[DataRequired()])
    date_created = IntegerField('Date Created', validators=[DataRequired()])
    file = FileField('Upload mp3 file', validators=[DataRequired()])
    album = SelectField('Album', coerce=int)

    def set_album_choices(self):
        return [(album.id, album.name) for album in Album.query.all()] or [(0, 'No Albums')]


    def populate_form(self, song):
        self.name.data = song.name
        self.lyrics.data = song.lyrics
        self.duration.data = song.duration
        self.date_created.data = song.date_created
        if song.album:
            self.album.data = song.album.id
        # Exclude the file field from form population

    def populate_obj_with_changes(self, song):
        song.name = self.name.data
        song.lyrics = self.lyrics.data
        song.duration = self.duration.data
        song.date_created = self.date_created.data
        if self.album.data:
            song.album_id = self.album.data

from flask import Flask, render_template, request
import os
app = Flask(__name__)
@auth.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        song_name = request.form.get('name')  # Correct the form field name
        lyrics = request.form.get('lyrics')
        duration = request.form.get('duration')
        date_created = request.form.get('date_created')
        album_id = request.form.get('album')

        UPLOAD_FOLDER = 'static'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        relative_file_path = os.path.relpath(file_path, app.root_path)
        new_song = Song(name=song_name, lyrics=lyrics, duration=duration, date_created=date_created, file=relative_file_path,album_id=album_id)
        db.session.add(new_song)
        db.session.commit()

        flash('Song Added Successfully! Redirecting to all songs page...', category='success')
        return redirect(url_for('auth.creator_page'))

    form = SongForm()
    form.album.choices = form.set_album_choices()  
    return render_template('add_song.html', form=form)

@auth.route('/edit_song/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = Song.query.get_or_404(song_id)
    form = SongForm()
    
    if request.method == 'POST':
        form.populate_obj_with_changes(song)  
        db.session.commit()
        return redirect(url_for('auth.edit_songs'))  

    form.populate_form(song)  
    form.album.choices = form.set_album_choices()  

    return render_template('edit_song.html', form=form, song=song)

@auth.route('/songs')
#@login_required
def songs():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM songs')
    songs = cursor.fetchall()

    conn.close()

    return render_template('songs.html', songs=songs)

@auth.route('/edit_songs')
#@login_required
def edit_songs():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM songs')
    songs = cursor.fetchall()

    conn.close()

    return render_template('edit_songs.html', songs=songs)


@auth.route('/delete_song/<int:song_id>', methods=['GET', 'POST'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)

    if request.method == 'POST':
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('auth.edit_songs'))
    return render_template('delete_song.html', song=song)



@auth.route('/playsong/<int:song_id>')
#@login_required
def playsong(song_id):

    song = Song.query.get_or_404(song_id)

    return render_template('playsong.html', song=song, user=current_user)



@auth.route('/create_playlist_user', methods=['GET', 'POST'])
#@login_required
def create_playlist_user():
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        selected_song_ids = request.form.getlist('selected_songs[]')
        user_id = request.form.get('user_id')
        new_playlist = Playlist(name=playlist_name,user_id=user_id)

        for song_id in selected_song_ids:
            song = session.query(Song).get(song_id)
            if song:
                new_playlist.songs.append(song)

        session.add(new_playlist)
        session.commit()
        songs = session.query(Song).all()

        return redirect(url_for('auth.open_playlist',playlist_id=new_playlist.id))  


    songs = Song.query.all()
    return render_template('create_playlist_user.html', songs=songs)


@auth.route('/create_playlist_creator', methods=['GET', 'POST'])
#@login_required
def create_playlist_creator():
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        selected_song_ids = request.form.getlist('selected_songs[]')
        user_id = request.form.get('user_id')
        new_playlist = Playlist(name=playlist_name,creator_id=user_id)

        for song_id in selected_song_ids:
            song = session.query(Song).get(song_id)
            if song:
                new_playlist.songs.append(song)

        session.add(new_playlist)
        session.commit()
        songs = session.query(Song).all()

        return redirect(url_for('auth.open_playlist',playlist_id=new_playlist.id))  


    songs = Song.query.all()
    return render_template('create_playlist_creator.html', songs=songs)

@auth.route('/search', methods=['GET', 'POST'])
#@login_required
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = search_songs(query)
    else:
        results = []

    return render_template('search.html',results=results)
Session = sessionmaker(bind=db)
def search_songs(query):
    song_results = (session.query(Song).filter(
            or_(
                or_(Song.artist.ilike(f'%{query}%'), Song.Genre.ilike(f'%{query}%')),
                or_(Song.rating.ilike(f'%{query}%'), Song.name.ilike(f'%{query}%'))
                )
                )
                .all()
                )

    album_results = (
        session.query(Album)
        .filter(
            or_(
                Album.artist.ilike(f'%{query}%'),
                Album.genre.ilike(f'%{query}%')
            )
        )
        .all()
    )
    session.close()
    return {
        'songs': song_results,
        'albums': album_results
    }


from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///instance/database.db', echo=True)

Session = sessionmaker(bind=engine)








from .models import Album
#@login_required
@auth.route('/create_album', methods=['GET','POST'])
def create_album():
    session = Session()

    if request.method == 'POST':
        # Get album details from the form
        album_name = request.form.get('name')
        artist = request.form.get('artist')
        genre = request.form.get('genre')
        date_created = request.form.get('date_created')
        selected_song_ids = request.form.getlist('selected_songs[]')

        # Create the album
        album = Album(name=album_name, artist=artist, genre=genre, date_created=date_created)

        # Associate selected songs with the album
        for song_id in selected_song_ids:
            song = session.query(Song).get(song_id)
            if song:  # Check if the song with the given ID exists
                album.songs.append(song)

        # Add the album to the session and commit changes
        session.add(album)
        session.commit()
        songs = session.query(Song).all()
        return render_template('create_album.html',songs=songs)

        # Retrieve songs for rendering the template
    songs = session.query(Song).all()

    return render_template('create_album.html', songs=songs)











@auth.route('/albums')
#@login_required
def albums():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # Fetch all songs from the database
    cursor.execute('SELECT * FROM albums')
    albums = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the HTML page with the list of songs
    return render_template('albums.html', albums=albums)




@auth.route('/open_album/<int:album_id>')
#@login_required
def open_album(album_id):

        # Connect to the SQLite database
    album = Album.query.get_or_404(album_id)
    songs = album.songs 

    return render_template('open_album.html', songs=songs)

@auth.route('/open_playlist/<int:playlist_id>')
#@login_required
def open_playlist(playlist_id):

        # Connect to the SQLite database
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = playlist.songs 

    return render_template('open_playlist.html', songs=songs,playlist=playlist)

@auth.route('/user_playlists/<string:user_id>')
#@login_required
def user_playlists(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    playlists = user.user_playlists 
    return render_template('user_playlists.html', playlists=playlists)

@auth.route('/del_playlist_user/<int:playlist_id>', methods=['GET', 'POST'])
def del_playlist_user(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)

    db.session.delete(playlist)
    db.session.commit()
    user_id = current_user.id
    return redirect(url_for('auth.user_playlists',user_id=user_id))

@auth.route('/creator_playlists/<string:user_id>')
#@login_required
def creator_playlists(user_id):
    # Connect to the SQLite database
    creator = Creator.query.filter_by(id=user_id).first_or_404()
    playlists = creator.creator_playlists 
    return render_template('creator_playlists.html', playlists=playlists)

@auth.route('/del_playlist_creator/<int:playlist_id>', methods=['GET', 'POST'])
def del_playlist_creator(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)

    db.session.delete(playlist)
    db.session.commit()

    return redirect(url_for('auth.creator_playlists',user_id=current_user.id))



from .models import Rating

@auth.route('/rate/<int:song_id>', methods=['POST'])
def rate(song_id):
    rating_value = int(request.form['rating'])
    user_id = int(request.form['user_id'])

    song = Song.query.get(song_id)
    if song:
        new_rating = Rating(rating=rating_value, user_id=user_id, song_id=song.id)
        db.session.add(new_rating)
        db.session.commit()

        # Update the average rating for the song
        song_ratings = [r.rating for r in song.ratings]
        average_rating = sum(song_ratings) / len(song_ratings) if song_ratings else 0
        song.rating = average_rating
        db.session.commit()

    return redirect(url_for('auth.playsong',song_id=song.id))



@auth.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
def edit_album(album_id):
    album = Album.query.get_or_404(album_id)
    all_songs = Song.query.all() 

    if request.method == 'POST':
        # Update album details
        album.name = request.form['name']
        album.artist = request.form['artist']
        album.genre = request.form['genre']
        album.date_created = request.form['date_created']

        # Update associated songs
        #selected_song_ids = request.form.getlist('selected_songs[]')
        selected_song_ids = [int(song_id) for song_id in request.form.getlist('selected_songs[]')]
        album.songs = Song.query.filter(Song.id.in_(selected_song_ids)).all()

        #for song_id in selected_song_ids:
         #   song = session.query(Song).get(song_id)
          #  if song:  # Check if the song with the given ID exists
           #     album.songs.append(song)


        db.session.commit()
        return redirect(url_for('auth.edit_albums'))  

    return render_template('edit_album.html', album=album, all_songs=all_songs)




@auth.route('/edit_albums')
#@login_required
def edit_albums():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM albums')
    albums = cursor.fetchall()

    conn.close()

    return render_template('edit_albums.html', albums=albums)


@auth.route('/delete_album/<int:album_id>', methods=['GET', 'POST'])
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)

    if request.method == 'POST':
        db.session.delete(album)
        db.session.commit()
        return redirect(url_for('auth.edit_albums'))
    return render_template('delete_album.html', album=album)


@auth.route('/blacklist/<int:creator_id>', methods=['GET', 'POST'])
def blacklist(creator_id):
    creator = Creator.query.get(creator_id)

    db.session.delete(creator)
    db.session.commit()

        # Append the creator to the 'blacklist' table
    blacklist_entry = Blacklist(email=creator.email,password=creator.password)
    db.session.add(blacklist_entry)
    db.session.commit()

    return redirect(url_for('auth.creators'))
@auth.route('/whitelist/<int:creator_id>', methods=['GET', 'POST'])
def whitelist(creator_id):
    creator = Blacklist.query.get(creator_id)

    db.session.delete(creator)
    db.session.commit()

        # Append the creator to the 'blacklist' table
    whitelist_entry = Creator(email=creator.email,password=creator.password)
    db.session.add(whitelist_entry)
    db.session.commit()

    return redirect(url_for('auth.creators'))

@auth.route('/creators')
#@login_required
def creators():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # Fetch all songs from the database
    cursor.execute('SELECT * FROM creator')
    creators = cursor.fetchall()

    cursor.execute('SELECT * FROM blacklist')
    blacklist = cursor.fetchall()
    # Close the database connection
    conn.close()

    # Render the HTML page with the list of songs
    return render_template('creators.html', creators=creators,blacklist=blacklist)


@auth.route('/users')
#@login_required
def users():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # Fetch all songs from the database
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    conn.close()
    # Render the HTML page with the list of songs
    return render_template('users.html', users=users)

@auth.route('/albums_page')
#@login_required
def albums_page():

    not_flagged = Album.query.filter_by(flag=False).all()
    flagged = Album.query.filter_by(flag=True).all()

    # Render the HTML page with the list of songs
    return render_template('albums_page.html',not_flagged=not_flagged, flagged=flagged)


@auth.route('/flag_album/<int:album_id>', methods=['GET', 'POST'])
def flag_album(album_id):
    album = Album.query.get(album_id)
    album.flag = True
    db.session.commit()

    return redirect(url_for('auth.albums_page'))

@auth.route('/remove_flag/<int:album_id>', methods=['GET', 'POST'])
def remove_flag(album_id):
    album = Album.query.get(album_id)

    album.flag = False
    db.session.commit()

    return redirect(url_for('auth.albums_page'))



@auth.route('/songs_page')
#@login_required
def songs_page():

    not_flagged = Song.query.filter_by(flag=False).all()
    flagged = Song.query.filter_by(flag=True).all()

    # Render the HTML page with the list of songs
    return render_template('songs_page.html',not_flagged=not_flagged, flagged=flagged)


@auth.route('/flag_song/<int:song_id>', methods=['GET', 'POST'])
def flag_song(song_id):
    song = Song.query.get(song_id)
    song.flag = True
    db.session.commit()

    return redirect(url_for('auth.songs_page'))

@auth.route('/remove_flag_song/<int:song_id>', methods=['GET', 'POST'])
def remove_flag_song(song_id):
    song = Song.query.get(song_id)

    song.flag = False
    db.session.commit()

    return redirect(url_for('auth.songs_page'))