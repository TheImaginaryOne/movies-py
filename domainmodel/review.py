from datetime import datetime

from domainmodel.movie import Movie


class Review:
    def __init__(self, movie, review_text, rating):
        self.movie: Movie = movie
        self.review_text: str = review_text
        self.rating: int = rating
        self.timestamp: datetime = datetime.now()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, r):
        if 0 < r <= 10:
            self._rating = r
        else:
            self._rating = None

    def __repr__(self):
        return f"<Review {self.movie}, {self.review_text}, {self._rating}, {self.timestamp}>"

    def __eq__(self, other: 'Review'):
        return self.movie == other.movie \
               and self.review_text == other.review_text \
               and self._rating == other._rating \
               and self.timestamp == other.timestamp
