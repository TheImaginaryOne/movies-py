from domainmodel.repository import MemoryRepository
from domainmodel.movie import Movie
from domainmodel.director import Director
from domainmodel.actor import Actor
from domainmodel.genre import Genre

d1 = Director("DJ Khaled")
d2 = Director("Angry Shrek")
a1 = Actor("Bill Nye")
a2 = Actor("Notch")
g1 = Genre("Sci-fi")
g2 = Genre("Fantasy")

m0 = Movie("The", 2020)

m1 = Movie("Tragedy", 2020)
m1.director = d1
m1.add_actor(a1)
m1.add_genre(g1)

m2 = Movie("of", 2020)

m3 = Movie("Darth", 2020)
m3.director = d1

m4 = Movie("Plagueis", 2020)
m4.add_actor(a1)
m4.add_actor(a2)
m4.add_genre(g1)

m5 = Movie("the", 2020)
m5.add_actor(a1)
m5.add_actor(a2)

m6 = Movie("Wise", 2020)
m6.director = d2
movies_mock = [m0, m1, m2, m3, m4, m5, m6]
rr = MemoryRepository(movies_mock, [], [], [])


def test_view_movies():
    assert rr.view_movies(0, 3) == ([m0, m1, m2], True)
    assert rr.view_movies(5, 80) == ([m5, m6], False)


def test_view_movies_filter():
    assert rr.view_movies(0, 3, d1.director_full_name, [], []) == ([m1, m3], False)
    assert rr.view_movies(0, 3, d2.director_full_name, [], []) == ([m6], False)


def test_view_movies_filter_actor():
    assert rr.view_movies(0, 3, "", [a1.actor_full_name, a2.actor_full_name], []) == ([m4, m5], False)
    assert rr.view_movies(0, 3, d1.director_full_name, [a1.actor_full_name], []) == ([m1], False)


def test_view_movies_filter_genre():
    assert rr.view_movies(0, 3, "", [a1.actor_full_name], [g1.genre_name]) == ([m1, m4], False)
