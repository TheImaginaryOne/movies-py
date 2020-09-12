from domainmodel.review import Review
from domainmodel.movie import Movie
from domainmodel.user import User


def test_basic():
    user1 = User('Martin', 'pw12345')
    assert user1.user_name == "martin"
    assert user1.__repr__() == "<User martin>"


def test_add_movie():
    movie = Movie("Shrek but every time he takes a STEP it gets 5% faster", 2010)
    movie.runtime_minutes = 9
    movie2 = Movie("The Bee Movie but its 20000x faster", 2010)
    movie2.runtime_minutes = 3
    user1 = User('Me', 'pw12345')

    user1.watch_movie(movie)
    assert user1.time_spent_watching_movies_minutes == 9
    user1.watch_movie(movie2)
    assert user1.time_spent_watching_movies_minutes == 12
    assert user1.watched_movies == [movie, movie2]

def test_duplicate_movie():
    movie = Movie("The Bee Movie but its 20000x faster", 2010)
    user1 = User('me', 'pwd')
    user1.watch_movie(movie)
    assert user1.watched_movies == [movie]
    user1.watch_movie(movie)
    assert user1.watched_movies == [movie]

def test_user_equality():
    user1 = User('Chewbacca', 'pp')
    user2 = User('Chewbacca', 'pp')
    user3 = User('a_bee', 'pp')
    assert user1 == user2
    assert user1 != user3


def test_add_review():
    user1 = User('Me', 'pw12345')
    movie2 = Movie("Star Wars", 1977)

    review = Review(movie2, "My car turned into the Millennium Falcon after showing the movie to it", 10)
    user1.add_review(review)
    assert user1.reviews == [review]

