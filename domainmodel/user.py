from domainmodel.movie import Movie
from domainmodel.review import Review


class User:
    def __init__(self, user_name, password):
        self.user_name: str = user_name
        self.password: str = password
        self.watched_movies: [Movie] = []
        self.reviews: [Review] = []
        self.time_spent_watching_movies_minutes: int = 0

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, u: str):
        self._user_name = u.lower().strip()

    def __repr__(self):
        return f"<User {self._user_name}>"

    def __eq__(self, other: 'User'):
        return self._user_name == other._user_name

    def __lt__(self, other: 'User'):
        return self._user_name < other._user_name

    def __hash__(self):
        return hash(self._user_name)

    def watch_movie(self, movie: Movie):
        self.watched_movies.append(movie)
        self.time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        self.reviews.append(review)
