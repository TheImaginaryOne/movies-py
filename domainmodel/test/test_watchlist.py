from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.watchlist import WatchList

movie = Movie("Bee Movie but its 19999x faster", 2300)
movie.runtime_minutes = 122
movie2 = Movie("Shrek but everytime someone blinks it gets faster", 2300)
movie2.runtime_minutes = 233
movie3 = Movie("The Lego Duplo Movie", 2300)

def test_add_movie():
    w = WatchList()
    w.add_movie(movie)
    assert w.first_movie_in_watchlist() == movie
    assert w.size() == 1
    w.add_movie(movie2)
    assert w.first_movie_in_watchlist() == movie
    assert w.size() == 2


def test_add_movie_twice():
    w = WatchList()
    w.add_movie(movie)
    assert w.size() == 1
    w.add_movie(movie)
    assert w.size() == 1


def test_remove_movie():
    w = WatchList()
    w.add_movie(movie)
    assert w.size() == 1
    w.remove_movie(movie2)
    assert w.size() == 1
    w.remove_movie(movie)
    assert w.size() == 0


def test_select_index():
    w = WatchList()
    w.add_movie(movie)
    w.add_movie(movie2)
    assert w.select_movie_to_watch(0) == movie
    assert w.select_movie_to_watch(1) == movie2
    assert w.select_movie_to_watch(2) is None
    assert w.select_movie_to_watch(-1) is None

def test_iterate():
    w = WatchList()
    w.add_movie(movie)
    w.add_movie(movie2)
    w.add_movie(movie3)
    assert list(w) == [movie, movie2, movie3]

def test_watch_movie():
    w = WatchList()
    w.add_movie(movie)
    w.add_movie(movie2)
    w.add_movie(movie3)
    user = User("bob", "pwd")
    w.watch_movie(user, 1)
    assert list(w) == [movie, movie3]
    assert user.time_spent_watching_movies_minutes == 233
    w.watch_movie(user, 0)
    assert list(w) == [movie3]
    assert user.time_spent_watching_movies_minutes == 355
