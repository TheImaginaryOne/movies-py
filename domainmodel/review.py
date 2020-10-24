from datetime import datetime

from domainmodel.movie import Movie


class Review:
    def __init__(self, movie, review_text, rating):
        self.movie_id = movie
        self.review_text: str = review_text
        self.rating: int = rating
        if 0 < rating <= 10:
            self.rating = rating
        else:
            self.rating = None
        self.timestamp: datetime = datetime.now()
        self.user_id = 0 # yes

#    @property
#    def rating(self):
#        return self._rating
#
#    @rating.setter
#    def rating(self, r):
#        if 0 < r <= 10:
#            self._rating = r
#        else:
#            self._rating = None

    def __repr__(self):
        return f"<Review {self.movie_id}, {self.review_text}, {self.rating}, {self.timestamp}>"

    def __eq__(self, other: 'Review'):
        return self.movie_id == other.movie_id \
               and self.review_text == other.review_text \
               and self.rating == other.rating \
               and self.timestamp == other.timestamp
