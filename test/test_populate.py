from test_common import client_with_db_data
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

def test_():
    client, repo = client_with_db_data()

    session = repo.session_factory()

    movie_count = session.query(Movie).count()
    assert movie_count == 100
    genre_count = session.query(Genre).count()
    assert genre_count == 18
    actor_count = session.query(Actor).count()
    assert actor_count == 320
    director_count = session.query(Director).count()
    assert director_count == 89
