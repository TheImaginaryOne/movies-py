from typing import Optional

from domainmodel.movie import Movie


class WatchList:
    def __init__(self):
        self.movies = []

    def add_movie(self, movie: Movie):
        if movie not in self.movies:
            self.movies.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.movies:
            self.movies.remove(movie)

    def select_movie_to_watch(self, index) -> Optional[Movie]:
        if 0 <= index < len(self.movies):
            return self.movies[index]
        return None

    def size(self) -> int:
        return len(self.movies)

    def first_movie_in_watchlist(self) -> Optional[Movie]:
        return self.select_movie_to_watch(0)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.movies):
            self.index += 1
            return self.movies[self.index - 1]
        else:
            raise StopIteration
