import csv

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.dataset_of_movies = []
        self.dataset_of_actors = []
        self.dataset_of_directors = []
        self.dataset_of_genres = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                #print(f"Movie {index} with title: {title}, release year {release_year}")
                m = Movie(title, release_year)
                m.description = row['Description']

                director = Director(row['Director'])
                try:
                    # if director exists, assign the same director object to the movie
                    index = self.dataset_of_directors.index(director)
                    director = self.dataset_of_directors[index]
                except ValueError:
                    self.dataset_of_directors.append(director)
                m.director = director

                m.votes = int(row['Votes'])
                m.rating = float(row['Rating'])
                m.runtime_minutes = int(row['Runtime (Minutes)'])
                if row['Metascore'] != 'N/A':
                    m.metascore = float(row['Metascore'])
                if row['Revenue (Millions)'] != 'N/A':
                    m.revenue = float(row['Revenue (Millions)'])

                for g in row['Genre'].split(","):
                    genre = Genre(g)
                    try:
                        index = self.dataset_of_genres.index(genre)
                        genre = self.dataset_of_genres[index]
                    except ValueError:
                        self.dataset_of_genres.append(genre)
                    m.add_genre(genre)

                for a in row['Actors'].split(","):
                    actor = Actor(a)
                    try:
                        index = self.dataset_of_actors.index(actor)
                        actor = self.dataset_of_actors[index]
                    except ValueError:
                        self.dataset_of_actors.append(actor)
                    m.add_actor(actor)

                if m not in self.dataset_of_movies:
                    self.dataset_of_movies.append(m)

