import requests
from flask import session, current_app

from domainmodel.movie import Movie
from domainmodel.repository import Repository
from domainmodel.review import Review


def get_movie(repository: Repository, index):
    return repository.get_movie(index)


def get_reviews(repository: Repository, movie_index):
    return repository.get_reviews(movie_index)


def add_review(repository: Repository, movie_index, review_text, rating):
    user_id = session['user']

    #movie = repository.get_movie(movie_index)
    review = Review(movie_index, review_text, rating)  # TODO!!!
    repository.add_review(user_id, review)
    current_app.logger.info(f"Review (user_id {user_id})")


MOVIES_ON_PAGE = 15


def view_movies(repository: Repository, page, director, actors, genres):
    actors = list(map(lambda x: x.strip(), actors))
    genres = list(map(lambda x: x.strip(), genres))

    return repository.view_movies(page * MOVIES_ON_PAGE, MOVIES_ON_PAGE, director, actors,
                                  genres)


def get_poster_url(movie: Movie):
    key = current_app.config.get('TMDB_KEY')
    if key is None:
        current_app.logger.error("TMDB_KEY not set")
        return ''
    try:
        response = requests.get(f'https://api.themoviedb.org/3/search/movie',
                                params={
                                    'api_key': key,
                                    'query': movie.title,
                                    'year': movie.release_year
                                })
        contents = response.json()
        poster_path = contents['results'][0]['poster_path']

        return f'http://image.tmdb.org/t/p/w500/{poster_path}'
    except ValueError as e:
        current_app.logger.error(f"TMDB response is not expected format: {e}")
        return ''
    except Exception as e:
        current_app.logger.error(f'Error fetching from TMDB: {e}')
        return ''
