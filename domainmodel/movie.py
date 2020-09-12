from typing import Optional

from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director


class Movie:
    def __init__(self, title: str, release_year: int):
        self._release_year: int = release_year if release_year >= 1900 else None
        self._title: str = title.strip() if title.strip() != "" else None
        self._description: str = ""
        self.director: Director = Director("")
        self.actors: [Actor] = []
        self.genres: [Genre] = []
        self._runtime_minutes: int = 0
        self._rating: float = 0
        self._votes: int = 0
        self._revenue: Optional[float] = None
        self._metascore: Optional[float] = None
        self.id = 0 # TODO

    @property
    def rating(self):
        """imdb score"""
        return self._rating

    @rating.setter
    def rating(self, rating):
        if 0 <= rating <= 10:
            self._rating = rating

    @property
    def votes(self):
        """imdb votes"""
        return self._votes

    @votes.setter
    def votes(self, votes):
        if 0 <= votes:
            self._votes = votes

    @property
    def revenue(self):
        return self._revenue

    @revenue.setter
    def revenue(self, revenue):
        # probably if the movie is terrible then revenue < 0
        #if 0 <= revenue:
        self._revenue = revenue

    @property
    def metascore(self):
        """metacritic score"""
        return self._metascore

    @metascore.setter
    def metascore(self, metascore):
        if 0 <= metascore:
            self._metascore = metascore

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, value: int):
        if value > 0:
            self._runtime_minutes = value
        else:
            raise ValueError

    # ONLY GET NO SET
    @property
    def release_year(self):
        return self._release_year

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        s = value.strip()
        self._description = s

    # ONLY GET NOT SET
    @property
    def title(self):
        return self._title

    def __eq__(self, other: 'Movie'):
        return self._title == other._title and self._release_year == other._release_year

    def __lt__(self, other: 'Movie'):
        if self._title == other._title:
            return self._release_year < other._release_year
        return self._title < other._title

    def __hash__(self):
        return hash((self._title, self._release_year))

    def __repr__(self):
        return f"<Movie {self._title}, {self._release_year}>"

    def add_actor(self, actor: Actor):
        if actor not in self.actors:
            self.actors.append(actor)

    def add_genre(self, genre: Genre):
        if genre not in self.genres:
            self.genres.append(genre)

    def remove_actor(self, actor: Actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def remove_genre(self, genre: Genre):
        if genre in self.genres:
            self.genres.remove(genre)

