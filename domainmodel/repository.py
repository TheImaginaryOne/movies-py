from abc import abstractmethod

from sqlalchemy.orm import Session, aliased, selectinload
from sqlalchemy.orm.exc import NoResultFound

from domainmodel.movie import Movie
from domainmodel.director import Director
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.orm import movie_actor, movie_genre
from domainmodel.review import Review
from domainmodel.user import User


class Repository:
    def __init__(self):
        self.movies = None
        self.actors = None
        self.directors = None
        self.genres = None
        self.users = None

    @abstractmethod
    def view_movies(self, start, number, director: str = "", actors=None, genres=None):
        if genres is None:
            genres = []
        if actors is None:
            actors = []

    @abstractmethod
    def add_user(self, username, password):
        pass

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def get_user(self, index):
        pass

    @abstractmethod
    def get_movie(self, index):
        pass

    @abstractmethod
    def get_reviews(self, movie_index) -> [(User, Review)]:
        pass

    @abstractmethod
    def add_review(self, user_id, review):
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
        for i, movie in enumerate(m):
            movie.id = i
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
        if movie_index < len(self.movies):
            reviews = []
            for user in self.users:
                user_reviews = list(filter(lambda u: u.movie_id == movie_index, user.reviews))
                if len(user_reviews) > 0:
                    reviews.append((user, user_reviews))

            return reviews
        return None

    def add_review(self, user_index, review):
        if user_index < len(self.users):
            self.users[user_index].add_review(review)
            return True
        return False

    def has_user(self, user_id):
        return 0 <= user_id < len(self.users)

    def login(self, username, password):
        users = list(filter(lambda u: u[1].username == username, enumerate(self.users)))

        if len(users) == 0:
            return None

        if users[0][1].verify_password(password):
            return users[0][0]  # return id of user


class DatabaseRepository(Repository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    # @property
    # def movies(self):
    #     return Session().query(User)

    @property
    def directors(self):
        l = self.session_factory().query(Director).all()
        return l

    @property
    def actors(self):
        return self.session_factory().query(Actor).all()

    @property
    def genres(self):
        return self.session_factory().query(Genre).all()

    def view_movies(self, start, number, director=None, actors=None, genres=None):
        session = self.session_factory()
        query = session.query(Movie)
        if director is not None and director != "":
            query = query.join(Director).filter(Director.full_name == director)

        for actor_name in actors:
            a = aliased(Actor)
            m = aliased(movie_actor)
            query = query.join(m, Movie.id == m.c.movie_id).join(a, m.c.actor_id == a.id)
            query = query.filter(a.full_name == actor_name)

        for genre_name in genres:
            g = aliased(Genre)
            mg = aliased(movie_genre)
            query = query.join(mg, Movie.id == mg.c.movie_id).join(g, mg.c.genre_id == g.id)
            query = query.filter(g.name == genre_name)

        count = query.count()
        # paginate
        query = query.options(selectinload(Movie.actors), selectinload(Movie.director))
        results = query.limit(number).offset(start).all()

        return results, start + number < count

    def add_user(self, username, password):
        session = self.session_factory()
        user = User(username, password)
        # username is converted appropriately when inserted
        # into User object.
        has_user = session.query(User)\
            .filter(User.username == user.username)\
            .count() > 0
        if has_user:
            return False

        session = self.session_factory()
        session.add(user)
        session.commit()
        return True

    def get_user(self, index):
        session = self.session_factory()
        try:
            return session.query(User).filter(User.id == index).one()
        except NoResultFound:
            return None

    def get_movie(self, index):
        session = self.session_factory()
        print(Movie.actors)
        try:
            # selectinload causes an eager load, ie. data is loaded
            # as soon as possible
            return session.query(Movie) \
                .filter(Movie.id == index)\
                .options(selectinload(Movie.actors),
                         selectinload(Movie.genres),
                         selectinload(Movie.director)
                         )\
                .one()
        except NoResultFound:
            return None

    def get_reviews(self, movie_index):
        session = self.session_factory()
        reviews = session.query(Review)\
                .join(Movie)\
                .filter(Movie.id == movie_index)\
                .order_by(Review.user_id)\
                .all()
        user_ids = [review.user_id for review in reviews]
        # reviews probably may not be grouped by users.... *shrugs*
        users = session.query(User)\
                .filter(User.id.in_(user_ids))\
                .order_by(User.id)\
                .all()
        #print(reviews)
        #print(users)

        import itertools

        z = zip(users, itertools.groupby(reviews, lambda x: x.user_id))
        l = list(map(lambda pair: (pair[0], list(pair[1][1])), z))
        return l

    def add_review(self, user_id, review):
        session = self.session_factory()
        if not self.has_user(user_id):
            return False

        review.user_id = user_id
        session.add(review)
        session.commit()
        return True

    def has_user(self, user_id):
        session = self.session_factory()
        return session.query(User).filter(User.id == user_id).count() > 0

    def login(self, username, password):
        session = self.session_factory()
        try:
            user = session.query(User).filter(User.username == username).one()

            if user.verify_password(password):
                return user.id  # return id of user
            return None
        except NoResultFound:
            return None
