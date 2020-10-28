from domainmodel.orm import metadata
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader

def populate_database(session_factory, database_engine, filename):
    metadata.drop_all(database_engine)
    metadata.create_all(database_engine)  # Conditionally create database tables.
    # populate data
    file_reader = MovieFileCSVReader(filename)
    file_reader.read_csv_file()

    session = session_factory()
    session.add_all(file_reader.dataset_of_movies)
    print(f"{len(file_reader.dataset_of_movies)} movies")
    session.commit()
