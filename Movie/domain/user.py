from typing import List, Iterable

class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name.strip().lower()
        self.__password = password
        self.__watched_movies = []
        self.__comments = []
        self.__time_spent_watching_movies_minutes: int = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @user_name.setter
    def user_name(self, name):
        if name == "" or type(name) is not str:
            self.__user_name = None
        else:
            self.__user_name = name.strip().lower()

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password):
        if isinstance(password, str):
            self.__password = password
        else:
            raise TypeError

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @watched_movies.setter
    def watched_movies(self, movie: list):
        if isinstance(movie, list):
            self.__watched_movies += movie
        else:
            raise TypeError

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self.__comments)

    @comments.setter
    def comments(self, reviews):
        if reviews == "" or type(reviews) is not str:
            self.__comments = None
        else:
            self.__comments = reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, mins: int):
        if isinstance(mins, int):
            self.__time_spent_watching_movies_minutes =  mins
        else:
            raise TypeError

    def __repr__(self) -> str:
        return "<User {} {}>".format(self.__user_name, self.__password)

    def __eq__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return False
        return self.__user_name == other.__user_name

    def __lt__(self, other: 'User') -> bool:
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie: 'Movie'):
        if isinstance(movie, 'Movie'):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
                self.__time_spent_watching_movies_minutes += movie.runtime_minutes
            else:
                pass
        else:
            raise TypeError

    def add_comment(self, comment: 'Comment'):
        self.__comments.append(comment)





