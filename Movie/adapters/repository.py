import abc
from typing import List
from datetime import date

from Movie.domain.actor import Actor
from Movie.domain.director import Director
from Movie.domain.genre import Genre
from Movie.domain.movie import Movie
from Movie.domain.comment import Comment
from Movie.domain.user import User
from Movie.domain.actor import Actor
from Movie.domain.director import Director


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, rank: int) -> Movie:
        """ Returns Movie from the repository.

        If there is no Movie, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self) -> List[Movie]:
        """ Returns list Movie from the repository.

        If there is no Movie, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_rank(self, target_rank: int) -> List[Movie]:
        """ Returns a Movies list that were published on target_rank.

        If there are no Movies on the given rank, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Article from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_genre(self, genre: Genre):
        """ Returns a list of Movies, whose genre match those in genre, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_actor(self, actor: Actor):
        """ Returns a list of Movies, whose actor match those in actor, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_director(self, director: Director):
        """ Returns a list of Movies, whose director match those in director, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_rank_of_previous_movie(self, movie: Movie):
        """ Returns the year of an Movie that immediately precedes movie.

        If movie is the first movie in the repository, this method returns None because there are no Movie
        on a previous year.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_rank_of_next_movie(self, movie: Movie):
        """ Returns the year of an Movie that immediately follows movie.

        If movie is the last Movie in the repository, this method returns None because there are no Movie
        on a later year.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds an actor to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self) -> List[Actor]:
        """ Returns the Actor stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self):
        """ Returns the director stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self):
        """ Returns the genre stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.movie is None or comment not in comment.movie.comments:
            raise RepositoryException('Comment not correctly attached to an Movie')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError







