from domainmodel.movie import Movie
from domainmodel.director import Director
from domainmodel.actor import Actor
from domainmodel.genre import Genre


class Repository:
    def __init__(self):
        self.movies = None
        self.actors = None
        self.directors = None
        self.genres = None

    def view_movies(self, start, number, director: str = "", actors=None, genres=None):
        if genres is None:
            genres = []
        if actors is None:
            actors = []


def filter_results(director, actors, genres):
    def x(m: Movie):
        return (director == "" or m.director == Director(director)) \
               and (actors is [] or all(Actor(a) in m.actors for a in actors)) \
               and (genres is [] or all(Genre(g) in m.genres for g in genres))

    return x


class MemoryRepository(Repository):
    def __init__(self, m, a, d, g):
        self.movies = m
        self.actors = a
        self.directors = d
        self.genres = g

    def view_movies(self, start, number, director="", actors=None, genres=None):
        # JANKY TODO
        if genres is None:
            genres = []
        if actors is None:
            actors = []
        results = list(filter(filter_results(director, actors, genres), self.movies))
        return results[start:start + number], start + number < len(results)
