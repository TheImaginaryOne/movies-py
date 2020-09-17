from flask import session, current_app

from domainmodel.repository import Repository
from domainmodel.review import Review


def get_movie(repository: Repository, index):
    return repository.get_movie(index)


def get_reviews(repository: Repository, movie_index):
    return repository.get_reviews(movie_index)


def add_review(repository: Repository, movie_index, review_text, rating):
    user_id = session['user']

    movie = repository.get_movie(movie_index)
    review = Review(movie, review_text, rating)  # TODO!!!
    repository.add_review(user_id, review)
    current_app.logger.info(f"Review (user_id {user_id})")


MOVIES_ON_PAGE = 15


def view_movies(repository: Repository, page, director, actors, genres):
    actors = list(map(lambda x: x.strip(), actors))
    genres = list(map(lambda x: x.strip(), genres))

    return repository.view_movies(page * MOVIES_ON_PAGE, MOVIES_ON_PAGE, director, actors,
                                  genres)
