from Movie.domain.genre import Genre
from Movie.domain.actor import Actor
from Movie.domain.director import Director
from Movie.domain.comment import Comment
from typing import List, Iterable


class Movie:
    def __init__(self, rank, title: str, description: str, year: int, duration: int,
                 rating: float, votes: int, revenue: float = None, metascore: int = None):

        self.__rank = rank
        self.__title = title
        self.__description = description
        self.__year = year
        self.__duration = duration
        self.__rating = rating
        self.__votes = votes
        self.__revenue = revenue
        self.__metascore = metascore
        self.__actors: List[Actor] = []
        self.__director: Director = None
        self.__genres: List[Genre] = []
        self.__comments: List[Comment] = []

    @property
    def rank(self) -> int:
        return self.__rank

    @rank.setter
    def rank(self, index: int):
        self.__rank = index

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        if title == "" or not isinstance(title, str):
            self.__title = None
        else:
            self.__title = title.strip()

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director: 'Director'):
        if isinstance(director, Director):
            self.__director = director
        else:
            raise TypeError

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, mins: int):
        if mins >= 0:
            self.__duration = mins
        else:
            raise ValueError

    @property
    def rating(self):
        return self.__rating

    @property
    def votes(self):
        return self.__votes

    @votes.setter
    def votes(self, vote: int):
        if type(vote) == int:
            self.__votes = vote

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, profit):
        if profit == "N/A":
            self.__revenue == "N/A"
        else:
            if type(self.__revenue) == float:
                self.__revenue = profit

    @property
    def metascore(self):
        return self.__metascore

    @metascore.setter
    def metascore(self, score):
        if score == "N/A":
            self.__metascore = "N/A"
        elif type(score) == int and 0 <= score <= 10:
            self.__metascore = score
        else:
            self.__metascore = "N/A"

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self.__comments)

    def add_comment(self, comment: 'Comment'):
        self.__comments.append(comment)

    def number_of_comments(self):
        return len(self.__comments)

    def __repr__(self) -> str:
        return "<Movie {}, {}>".format(self.__title, self.__year)

    def __eq__(self, other: 'Movie') -> bool:
        return self.__rank == other.__rank

    def __lt__(self, other):
        return self.__rank < other.rank

    def __hash__(self):
        return hash((self.__title, self.__year))

    def add_actor(self, actor: 'Actor'):
        if isinstance(actor, Actor):
            self.__actors.append(actor)
        else:
            raise TypeError

    def remove_actor(self, actor: 'Actor'):
        if isinstance(actor, Actor):
            if actor in self.__actors:
                self.__actors.remove(actor)
            else:
                pass
        else:
            raise TypeError

    def add_genre(self, genre: 'Genre'):
        if isinstance(genre, Genre):
            self.__genres.append(genre)
        else:
            raise TypeError

    def remove_genre(self, genre: 'Genre'):
        if isinstance(genre, Genre):
            if genre in self.__genres:
                self.__genres.remove(genre)
            else:
                pass
        else:
            raise TypeError




