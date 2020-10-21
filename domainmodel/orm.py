from sqlalchemy import MetaData, Table, Integer, Column, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie
from domainmodel.review import Review
from domainmodel.user import User

metadata = MetaData()

user = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), unique=True, nullable=False),
)

actor = Table(
    'actor', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255)),
)

director = Table(
    'director', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255)),
)

genre = Table(
    'genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255)),
)

movie = Table(
    'movie', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('description', String()),
    Column('runtime_minutes', Integer),
    Column('director_id', ForeignKey('director.id')),
    Column('rating', Float),
    Column('votes', Integer),
    Column('revenue', Float),
    Column('metascore', Float),
)

movie_actor = Table(
    'movie_actor', metadata,
    Column('actor_id', ForeignKey('actor.id'), primary_key=True),
    Column('movie_id', ForeignKey('movie.id'), primary_key=True),
)

movie_genre = Table(
    'movie_genre', metadata,
    Column('genre_id', ForeignKey('genre.id'), primary_key=True),
    Column('movie_id', ForeignKey('movie.id'), primary_key=True),
)

review = Table(
    'review', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('user.id')),
    Column('movie_id', ForeignKey('movie.id')),
    Column('review_text', String()),
    Column('rating', Integer()),
    Column('timestamp', DateTime())
)


def map_model():
    mapper(User, user)
    mapper(Actor, actor)
    mapper(Director, director)
    mapper(Genre, genre)
    mapper(Movie, movie, properties={
        'director': relationship(Director),
        'genres': relationship(Genre, secondary=movie_genre),
        'actors': relationship(Actor, secondary=movie_actor),
    })
    #mapper(Review, review, properties={
    #    'movie': relationship(Movie),
    #    'user': relationship(User),
    #})
