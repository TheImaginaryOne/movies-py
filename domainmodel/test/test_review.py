from domainmodel.movie import Movie
from domainmodel.review import Review

import pytest


def test_basic():
    # https://ruinmyweek.com/lists/funny-one-star-movie-reviews/4/
    movie = Movie("The Jungle Book", 2010)
    review_text = "It's a film not a book very disappointed"
    rating = 1
    review = Review(movie, review_text, rating)
    review2 = Review(movie, review_text, rating)  # different timestamp
    review3 = Review(movie, review_text, rating)  # different timestamp
    review3.timestamp = review.timestamp

    assert review.__repr__() == f"<Review <Movie The Jungle Book, 2010>, {review_text}, 1, {review.timestamp}>"

    assert review.review_text == review_text
    assert review.rating == rating
    # equality
    assert review2 != review
    assert review == review3


def test_rating_range():
    movie = Movie("Shrek", 2010)
    review_text = "Shrek good"
    review = Review(movie, review_text, 11)
    assert review.rating is None
    review = Review(movie, review_text, 0)
    assert review.rating is None
    review = Review(movie, review_text, 3)
    assert review.rating == 3
