import pytest

from wsgi import create_app
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.repository import MemoryRepository, DatabaseRepository
from domainmodel.orm import map_model
from domainmodel.util import populate_database
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy import create_engine

@pytest.fixture
def client():
    return create_app(MemoryRepository([], [], [], []),
                      {'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SECRET_KEY': 'test'}).test_client()


def client_with_data():
    filename = 'datafiles/Data100Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    repository = MemoryRepository(movie_file_reader.dataset_of_movies,
                                  movie_file_reader.dataset_of_actors,
                                  movie_file_reader.dataset_of_directors,
                                  movie_file_reader.dataset_of_genres)
    return create_app(repository,
                      {'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SECRET_KEY': 'test'}).test_client(), repository

def client_with_db_empty():
    clear_mappers()
    database_engine = create_engine('sqlite:///')
    map_model()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    repository = DatabaseRepository(session_factory)

    return create_app(repository,
                      {'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SECRET_KEY': 'test'}).test_client(), repository

def client_with_db_data():
    clear_mappers()
    filename = 'datafiles/Data100Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    database_engine = create_engine('sqlite:///')
    map_model()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    populate_database(session_factory, database_engine, filename)

    repository = DatabaseRepository(session_factory)

    return create_app(repository,
                      {'TESTING': True, 'WTF_CSRF_ENABLED': False, 'SECRET_KEY': 'test'}).test_client(), repository
