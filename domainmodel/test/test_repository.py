from domainmodel.repository import MemoryRepository
from domainmodel.movie import Movie
from domainmodel.director import Director
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.user import User
from domainmodel.review import Review

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
    assert rr.view_movies(0, 3, d1.full_name, [], []) == ([m1, m3], False)
    assert rr.view_movies(0, 3, d2.full_name, [], []) == ([m6], False)


def test_view_movies_filter_actor():
    assert rr.view_movies(0, 3, "", [a1.full_name, a2.full_name], []) == ([m4, m5], False)
    assert rr.view_movies(0, 3, d1.full_name, [a1.full_name], []) == ([m1], False)


def test_view_movies_filter_genre():
    assert rr.view_movies(0, 3, "", [a1.full_name], [g1.name]) == ([m1, m4], False)


def test_add_user():
    repo = MemoryRepository(movies_mock, [], [], [])

    assert repo.add_user("bob", "pass123")
    assert not repo.add_user("bob", "pass12")  # duplicate user
    assert repo.add_user("bobb", "pass123")


def test_user_login():
    repo = MemoryRepository(movies_mock, [], [], [])

    assert repo.add_user("bob", "pass123")
    assert repo.add_user("bobb", "pass12")

    assert repo.login("bob", "pass123") == 0
    assert repo.login("bobb", "pass123") is None
    assert repo.login("bobb", "pass12") == 1
    assert repo.login("shrek", "pass123") is None
    assert repo.login("bob", "pass12344") is None

def test_user_index():
    repo = MemoryRepository(movies_mock, [], [], [])

    assert repo.add_user("a", "c")
    assert repo.add_user("b", "d")
    assert repo.get_user(0) == User("a", "c")
    assert repo.get_user(1) == User("b", "d")
    assert repo.get_user(2) is None

def test_add_review():
    repo = MemoryRepository(movies_mock, [], [], [])
    u1, u2 = User("bob", "pass123"), User("bobb", "pass12")

    assert repo.add_user("bob", "pass123")
    assert repo.add_user("bobb", "pass12")

    r1 = Review(1, "Darth Plagueis was dumb, why couldn't he stop his apprentice??!!", 3)
    r2 = Review(2, "The Sith did nothing wrong, Jedis just spread fake news", 7)
    r3 = Review(2, "Star Wars is silly", 1)
    r4 = Review(2, "Oops the previous review was written by my cat, Star Wars is wonderful", 9)

    # user_id, review
    repo.add_review(0, r1)
    repo.add_review(0, r2)
    repo.add_review(1, r3)
    repo.add_review(1, r4)

    # review for the movie m1 of id "1"
    assert repo.get_reviews(1) == [(u1, [r1])]
    assert repo.get_reviews(2) == [(u1, [r2]), (u2, [r3, r4])]
