from domainmodel.movie import Movie
from domainmodel.review import Review
from passlib.hash import pbkdf2_sha256 as hasher


class User:
    def __init__(self, user_name, password):
        self.username: str = user_name.lower()
        self.password_hash: str = hasher.hash(password)
        self.watched_movies: [Movie] = []
        self.reviews: [Review] = []
        self.time_spent_watching_movies_minutes: int = 0

   # @property
   # def username(self):
   #     return self.username

   # @username.setter
   # def username(self, u: str):
   #     self.username = u.lower().strip()

    def __repr__(self):
        return f"<User {self.username}>"

    def __eq__(self, other: 'User'):
        return self.username == other.username
    
    def verify_password(self, password):
        return hasher.verify(password, self.password_hash)

    def __lt__(self, other: 'User'):
        return self.username < other.username

    def __hash__(self):
        return hash(self.username)

    def watch_movie(self, movie: Movie):
        if movie not in self.watched_movies:
            self.watched_movies.append(movie)
            self.time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        self.reviews.append(review)
