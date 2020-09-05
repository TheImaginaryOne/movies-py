from domainmodel.movie import Movie


class Repository:
    def view_movies(self, start, number):
        pass


class MemoryRepository(Repository):
    def __init__(self, m):
        self.movies: [Movie] = m
        self.actors = m
        self.directors = m
        self.genres = m

    def view_movies(self, start, number):
        return self.movies[start:start + number]
