
class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.name = None
        else:
            self.name = genre_name.strip()

    def __repr__(self):
        return f"<Genre {self.name}>"

    def __eq__(self, other: 'Genre') -> bool:
        return self.name == other.name

    def __lt__(self, other: 'Genre') -> bool:
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)
