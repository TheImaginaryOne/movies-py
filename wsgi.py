import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.orm import map_model, metadata
from domainmodel.repository import MemoryRepository, DatabaseRepository
from web import movies, user, setup_app

def create_app(test_config=None):
    app = Flask(__name__)
    if 'CONFIG' in os.environ:
        app.config.from_envvar('CONFIG')
    if app.debug:
        app.secret_key = 'TEST'

    if test_config is not None:
        app.config.from_mapping(test_config)

    filename = 'datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    repository = None
    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository instance for a memory-based repository.
        repository = MemoryRepository(movie_file_reader.dataset_of_movies,
                                      movie_file_reader.dataset_of_actors,
                                      movie_file_reader.dataset_of_directors,
                                      movie_file_reader.dataset_of_genres)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        # database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri,
                                        connect_args={"check_same_thread": False},
                                        poolclass=NullPool,
                                        )

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            # For testing, or first-time use of the web application, reinitialise the database.
            # clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            # for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
            #     database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            #map_model_to_tables()

            #database_repository.populate(database_engine, data_path)

        else:
            pass
            # Solely generate mappings that map domain model classes to the database tables.
            # map_model_to_tables()
        map_model()

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repository = DatabaseRepository(session_factory)

    app.register_blueprint(movies.movies_blueprint(repository))
    app.register_blueprint(user.blueprint(repository))
    setup_app(app)
    user.inject_current_user(app, repository)

    if app.debug:
        (u, p) = ("user1234", "pass1234")
        repository.add_user(u, p)
    return app


def init():

    app = create_app()
    return app

app = init()
