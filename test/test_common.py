import pytest

from cs235init import create_app
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.repository import MemoryRepository


@pytest.fixture
def client():
    return create_app(MemoryRepository([], [], [], []), {'TESTING': True, 'WTF_CSRF_ENABLED': False}).test_client()


def client_with_data():
    filename = 'datafiles/Data100Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    repository = MemoryRepository(movie_file_reader.dataset_of_movies,
                                  movie_file_reader.dataset_of_actors,
                                  movie_file_reader.dataset_of_directors,
                                  movie_file_reader.dataset_of_genres)
    return create_app(repository, {'TESTING': True, 'WTF_CSRF_ENABLED': False}).test_client(), repository
