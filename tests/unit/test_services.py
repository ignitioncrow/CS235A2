from datetime import date

import pytest

from Movie.authentication.services import AuthenticationException
from Movie.movie import services as news_services
from Movie.authentication import services as auth_services
from Movie.movie.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_rank = 3
    comment_text = 'i like this movie'
    username = 'fmercury'

    # Call the service layer to add the comment.
    news_services.add_comment(movie_rank, comment_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    comments_as_dict = news_services.get_comments_for_movie(movie_rank, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
        None) is not None


def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie_rank = 1002
    comment_text = "i like this movie"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.NonExistentMovieException):
        news_services.add_comment(movie_rank, comment_text, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_rank = 1
    comment_text = 'waste of time'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(news_services.UnknownUserException):
        news_services.add_comment(movie_rank, comment_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_rank = 1

    movie_as_dict = news_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['title'] == 'Guardians of the Galaxy'
    assert movie_as_dict['description'] == 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    assert movie_as_dict['year'] == 2014
    assert movie_as_dict['duration'] == 121
    assert movie_as_dict['rating'] == 8.1
    assert len(movie_as_dict['comments']) == 3
    assert movie_as_dict['votes'] == 757074
    assert movie_as_dict['revenue'] == '333.13'
    assert movie_as_dict['metascore'] =='76'


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 1001

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(news_services.NonExistentMovieException):
        news_services.get_movie(movie_rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = news_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = news_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 1000


def test_get_movies_by_rank_with_one_rank(in_memory_repo):
    target_rank = 1

    movie_as_dict, prev_rank, next_rank = news_services.get_movie_by_rank(target_rank, in_memory_repo)

    assert len(movie_as_dict) == 1
    assert movie_as_dict[0]['rank'] == 1

    assert prev_rank is None
    assert next_rank == 2


def test_get_comments_for_movie(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_movie(1, in_memory_repo)

    # Check that 3 comments were returned for movie with rank 1.
    assert len(comments_as_dict) == 3

    # Check that the comments relate to the article whose id is 1.
    movie_rank = [comment['article_id'] for comment in comments_as_dict]
    movie_rank = set(movie_rank)
    assert 1 in movie_rank and len(movie_rank) == 1


def test_get_movies_by_rank_with_non_existent_rank(in_memory_repo):
    target_date = 1001

    with pytest.raises(ValueError):
        news_services.get_movie_by_rank(target_date, in_memory_repo)



def test_get_comments_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        comments_as_dict = news_services.get_comments_for_movie(1001, in_memory_repo)


def test_get_comments_for_article_without_comments(in_memory_repo):
    comments_as_dict = news_services.get_comments_for_movie(4, in_memory_repo)
    assert len(comments_as_dict) == 0

