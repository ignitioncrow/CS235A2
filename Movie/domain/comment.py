from datetime import datetime
from Movie.domain.user import User


class Comment:
    def __init__(self, user: User, movie, comment: str, timestamp: datetime):
        self._user: User = user
        self._movie = movie
        self._comment: Comment = comment
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self):
        return self._movie

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def timestamp(self) -> str:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other._user == self._user and other._movie == self._movie and other._comment == self._comment and other._timestamp == self._timestamp


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie, timestamp: datetime = datetime.today()):
    comment = Comment(user, movie, comment_text, timestamp)
    user.add_comment(comment)
    movie.add_comment(comment)
    return comment
