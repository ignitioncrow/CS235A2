from datetime import date
from Movie.domain.genre import Genre
from Movie.domain.actor import Actor
from Movie.domain.director import Director
from Movie.domain.comment import Comment, make_comment
from Movie.domain.movie import Movie
from Movie.domain.user import User


import pytest


@pytest.fixture()
def movie():
    return Movie(
        1,
        "Guardians of the Galaxy",
        "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.",
        2014,
        121,
        8.1,
        757074,
        333.13,
        76
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie: Movie):
    assert movie.rank == 1
    assert movie.title == 'Guardians of the Galaxy'
    assert movie.description == 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    assert movie.year == 2014
    assert movie.duration == 121
    assert movie.rating == 8.1
    assert movie.votes == 757074
    assert movie.revenue == 333.13
    assert movie.metascore == 76
    assert repr(movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_article_less_than_operator():
    movie_1 = Movie(
        1, None, None, 0, 0, 0, 0, None, None
    )

    movie_2 = Movie(
        2, None, None, 0, 0, 0, 0, None, None
    )

    assert movie_1 < movie_2


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'enjoyable movie'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the Article.
    assert comment.movie is movie





