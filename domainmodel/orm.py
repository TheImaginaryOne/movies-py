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
    Column('password_hash', String(255), nullable=False),
)

actor = Table(
    'actor', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), unique=True),
)

director = Table(
    'director', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), unique=True),
)

genre = Table(
    'genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True),
)

movie = Table(
    'movie', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('release_year', Integer),
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
        '_release_year': movie.c.release_year,
        '_title': movie.c.title,
        '_description': movie.c.description,
        '_runtime_minutes': movie.c.runtime_minutes,
        '_rating': movie.c.rating,
        '_votes': movie.c.votes,
        '_revenue': movie.c.revenue,
        '_metascore': movie.c.metascore,
    })
    #mapper(Review, review, properties={
    #    'movie': relationship(Movie),
    #    'user': relationship(User),
    #})
