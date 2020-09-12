from domainmodel.movie import Movie
from domainmodel.director import Director
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.review import Review
from domainmodel.user import User


class Repository:
    def __init__(self):
        self.movies = None
        self.actors = None
        self.directors = None
        self.genres = None
        self.users = None

    def view_movies(self, start, number, director: str = "", actors=None, genres=None):
        if genres is None:
            genres = []
        if actors is None:
            actors = []

    def add_user(self, username, password):
        pass

    def login(self, username, password):
        pass

    def get_user(self, index):
        pass

    def get_movie(self, index):
        pass

    def get_reviews(self, movie_index) -> [(User, Review)]:
        pass

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
        self.users = []

    def view_movies(self, start, number, director=None, actors=None, genres=None):
        # JANKY TODO
        if director is None:
            director = ""
        if genres is None:
            genres = []
        if actors is None:
            actors = []
        results = list(filter(filter_results(director, actors, genres), self.movies))
        return results[start:start + number], start + number < len(results)

    def add_user(self, username, password):
        uu = User(username, password)
        if uu not in self.users:
            self.users.append(uu)
            return True  # success
        else:
            return False  # failure - user exists!

    def get_user(self, index):
        if index < len(self.users):
            return self.users[index]
        return None

    def get_movie(self, index):
        if index < len(self.movies):
            return self.movies[index]
        return None

    def get_reviews(self, movie_index):
        reviews = []
        if movie_index < len(self.movies):
            for user in self.users:
                review = next(filter(lambda u: u.movie == self.movies[movie_index], user.reviews), None)
                if review is not None:
                    reviews.append((user, review))

            return reviews
        return None

    def add_review(self, user_index, review):
        if user_index < len(self.users):
            self.users[user_index].add_review(review)
            return True
        return False

    def login(self, username, password):
        users = list(filter(lambda u: u[1].user_name == username, enumerate(self.users)))

        if len(users) == 0:
            return None

        if users[0][1].password == password:
            return users[0][0]  # return id of user
