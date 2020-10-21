
class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.full_name = None
        else:
            self.full_name = director_full_name.strip()

    # @property
    # def full_name(self) -> str:
    #     return self.full_name

    def __repr__(self):
        return f"<Director {self.full_name}>"

    def __eq__(self, other: 'Director') -> bool:
        return self.full_name == other.full_name

    def __lt__(self, other: 'Director') -> bool:
        return self.full_name < other.full_name

    def __hash__(self):
        return hash(self.full_name)


class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.full_name is None
        director3 = Director(42)
        assert director3.full_name is None
