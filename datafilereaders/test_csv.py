import pathlib

from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie


def test_basic_csv():
    reader = MovieFileCSVReader(pathlib.Path(__file__).parent.joinpath("test.csv"))
    reader.read_csv_file()

    m1 = reader.dataset_of_movies[0]
    assert m1.title == "Darth"
    assert m1.release_year == 2014
    assert m1.genres == [Genre("Plagueis"), Genre("The W")]
    assert m1.description == "ise"
    assert m1.director == Director("Darth Vader")
    assert m1.actors == [Actor("Luke"), Actor("R2-D2"), Actor("Leia")]

def test_code_runner():
    filename = pathlib.Path(__file__).parent.parent.joinpath('datafiles/Data1000Movies.csv')
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    assert len(movie_file_reader.dataset_of_movies) == 1000
    assert len(movie_file_reader.dataset_of_actors) == 1985
    assert len(movie_file_reader.dataset_of_directors) == 644
    assert len(movie_file_reader.dataset_of_genres) == 20