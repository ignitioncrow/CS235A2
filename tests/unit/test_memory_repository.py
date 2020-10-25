from datetime import date, datetime
from typing import List

import pytest

from Movie.domain.genre import Genre
from Movie.domain.actor import Actor
from Movie.domain.director import Director
from Movie.domain.comment import Comment, make_comment
from Movie.domain.movie import Movie
from Movie.domain.user import User
from Movie.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        1001,
        'Some Movie',
        'yes some movie',
        2015,
        100,
        5.4,
        1234,
        543.3,
        67
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the movie is commented as expected.
    comment_one = [comment for comment in movie.comments if comment.comment == 'This movie is truly a lot of fun'][
        0]

    assert comment_one.user.user_name == 'fmercury'



def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_article(1001)
    assert movie is None


def test_repository_can_retrieve_movies_by_rank(in_memory_repo):
    movie = in_memory_repo.get_movie_by_rank(1)

    # Check that the query returned 3 Articles.
    assert movie[0].title == 'Guardians of the Galaxy'
    assert movie[0].year == 2014
    assert movie[0].rating == 8.1
    assert movie[0].rank == 1

def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_returns_an_empty_list_for_non_existent_ranks(in_memory_repo):
    movie = in_memory_repo.get_movie_by_rank(1002)
    assert movie == list()


def test_repository_returns_rank_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(4)
    previous_rank = in_memory_repo.get_rank_of_previous_movie(movie)

    assert previous_rank == 3


def test_repository_returns_none_when_there_are_no_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_rank = in_memory_repo.get_rank_of_previous_rank(movie)

    assert previous_rank is None


def test_repository_returns_rank_of_next_rank(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_rank = in_memory_repo.get_rank_of_next_movie(movie)

    assert next_rank == 4


def test_repository_returns_none_when_there_are_no_subsequent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1000)
    next_rank = in_memory_repo.get_rank_of_next_rank(movie)

    assert next_rank is None


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = make_comment("will watch it again", user, movie)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    comment = Comment(None, movie, "love this", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    comment = Comment(None, movie, "love it", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 4



