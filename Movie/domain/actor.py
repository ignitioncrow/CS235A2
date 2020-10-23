class Actor:
    def __init__(self, actor_full_name: str):
        self.__actor_colleague_li = []
        if actor_full_name == "" or type(actor_full_name) != str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @actor_full_name.setter
    def actor_full_name(self, other: str):
        self.__actor_full_name = other

    def __repr__(self) -> str:
        return "<Actor {}>".format(self.__actor_full_name)

    def __eq__(self, other: 'Actor') -> bool:
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other: 'Actor') -> bool:
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague: 'Actor'):
        if isinstance(colleague, Actor):
            self.__actor_colleague_li.append(colleague)
        else:
            raise TypeError

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        if isinstance(colleague, Actor) and colleague in self.__actor_colleague_li:
            return True
        else:
            return False


