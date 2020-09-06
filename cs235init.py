from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.user import User, Review, Movie
from domainmodel.repository import MemoryRepository
from flask import Flask
from web.movies import movies_blueprint
app = Flask(__name__)
app.secret_key = "TODO"

def main():
    filename = 'datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()
    repository = MemoryRepository(movie_file_reader.dataset_of_movies,
                                  movie_file_reader.dataset_of_actors,
                                  movie_file_reader.dataset_of_directors,
                                  movie_file_reader.dataset_of_genres)
    app.register_blueprint(movies_blueprint(repository))

main()