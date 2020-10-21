
class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.colleagues = []

    @property
    def full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other: 'Actor') -> bool:
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other: 'Actor') -> bool:
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor'):
        self.colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor'):
        return colleague in self.colleagues
