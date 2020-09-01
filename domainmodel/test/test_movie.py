import pytest

from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie


def test_basic():
    movie = Movie("Moana", 2015)
    assert str(movie) == "<Movie Moana, 2015>"

    director = Director("Ron Clements")
    movie.director = director
    assert movie.director == Director("Ron Clements")

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert movie.actors == actors

    movie.runtime_minutes = 107
    assert movie.runtime_minutes == 107


# https://knowyourmeme.com/memes/the-tragedy-of-darth-plagueis-the-wise
def test_year():
    assert Movie("Did you ever hear", 1899).release_year is None

    assert Movie("the tragedy of Darth", 1900).release_year == 1900


def test_name():
    assert Movie("  ", 2010).title is None

    assert Movie("Plagueis the Wise?", 2010).title == "Plagueis the Wise?"

    m = Movie("  I thought not.   ", 2010)
    assert m.title == "I thought not."


def test_desc():
    m2 = Movie("the Jedi would tell you.", 2010)
    m2.description = " It's a Sith Legend.  "
    assert m2.description == "It's a Sith Legend."


def test_movie_equality():
    a = Movie("Star Wars 10", 2050)
    b = Movie("Star Wars 10", 2050)
    c = Movie("Star Wars 10", 2051)
    d = Movie("Star Wars 11", 2050)
    b.runtime_minutes = 1000
    a.runtime_minutes = 2000
    # must only compare name and release year
    assert a == b
    assert a != c
    assert d != a


def test_movie_hash():
    a = Movie("Star Wars 10", 2050)
    b = Movie("Star Wars 10", 2050)
    c = Movie("Star Wars 10", 2051)
    d = Movie("Star Wars 11", 2050)
    b.runtime_minutes = 1000
    a.runtime_minutes = 2000
    # must only compare name and release year
    assert hash(a) == hash(b)
    assert hash(a) != hash(c)
    assert hash(d) != hash(a)


def test_movie_lt():
    a = Movie("Did you ever hear", 2000)
    b = Movie("the tragedy of Darth Plagueis the wise?", 1990)

    c = Movie("Did you ever hear", 2003)

    assert a < b
    assert a < c


def test_movie_set():
    a = Movie("I thought not.", 2000)
    b = Movie("It's not a story", 5050)
    ssss = set()
    ssss.add(a)
    ssss.add(b)
    ssss.add(b)
    ssss.add(a)
    assert len(ssss) == 2

    assert a in ssss
    assert b in ssss
    assert Movie("the Jedi would tell you.", 7000) not in ssss


def test_runtime_minutes():
    aa = Movie("mayday", 2000)
    aa.runtime_minutes = 1
    assert aa.runtime_minutes == 1

    with pytest.raises(ValueError):
        aa.runtime_minutes = 0
    with pytest.raises(ValueError):
        aa.runtime_minutes = -1


def test_actors():
    aa = Movie("Emu Wars", 2000)

    actor1 = Actor("Rick Astley")
    actor2 = Actor("Voldemort")
    actor3 = Actor("Winnie the Pooh")
    aa.add_actor(actor1)
    aa.add_actor(actor2)
    aa.add_actor(actor2)

    assert aa.actors == [actor1, actor2]

    aa.remove_actor(actor1)
    aa.remove_actor(actor3)
    assert aa.actors == [actor2]


def test_genre():
    aa = Movie("help", 2000)

    genre1 = Genre("scifi")
    genre2 = Genre("animation")
    aa.add_genre(genre1)
    aa.add_genre(genre1)
    aa.add_genre(genre2)
    aa.add_genre(genre1)

    assert aa.genres == [genre1, genre2]

    aa.remove_genre(genre1)
    aa.remove_genre(Genre("drama"))
    assert aa.genres == [genre2]
    aa.remove_genre(genre2)

    assert aa.genres == []


def test_movie_rating():
    mm = Movie("Star Wars The Third Gathers: Backstroke of the West", 2000)
    mm.rating = 6.3
    assert mm.rating == 6.3
    mm.rating = -1
    assert mm.rating == 6.3
    mm.rating = 11
    assert mm.rating == 6.3


def test_movie_revenue():
    mm = Movie("Star Wars The Third Gathers: Backstroke of the West", 2000)
    mm.revenue = 61.3
    assert mm.revenue == 61.3


def test_movie_votes():
    mm = Movie("Star Wars The Third Gathers: Backstroke of the West", 2000)
    mm.votes = 600
    assert mm.votes == 600
    mm.votes = -1
    assert mm.votes == 600


def test_movie_metascore():
    mm = Movie("Star Wars The Third Gathers: Backstroke of the West", 2000)
    mm.metascore = 43.3
    assert mm.metascore == 43.3
    mm.metascore = -1
    assert mm.metascore == 43.3
