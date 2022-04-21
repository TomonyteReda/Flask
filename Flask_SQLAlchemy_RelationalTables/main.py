import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') + '?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)


book_author_table = db.Table('book_authors',
                             db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                             db.Column('author_id', db.Integer, db.ForeignKey('authors.id')))


book_genre_table = db.Table('book_genres',
                            db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                            db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')))


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    rating = db.Column(db.Integer)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    authors = db.relationship('Author', secondary=book_author_table, backref='books')
    genres = db.relationship('Genre', secondary=book_genre_table, backref='books')

    def __init__(self, title, rating, publisher_id):
        self.title = title
        self.rating = rating
        self.publisher_id = publisher_id

    def __repr__(self):
        return f'{self.title} {self.rating}'



class Publisher(db.Model):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    books = db.relationship('Book', backref='publisher')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(300))

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def __repr__(self):
        return f'{self.fname} {self.lname}'


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(150))

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f'{self.genre}'

