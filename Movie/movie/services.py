from typing import List, Iterable

from Movie.adapters.repository import AbstractRepository
from Movie.domain.comment import make_comment, Comment
from Movie.domain.movie import Movie
from Movie.domain.genre import Genre


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(movie_rank: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, movie)

    # Update the repository.
    repo.add_comment(comment)


def get_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    first_movie = repo.get_first_movie()

    return movie_to_dict(first_movie)


def get_last_movie(repo: AbstractRepository):
    last_movie = repo.get_last_movie()
    return movie_to_dict(last_movie)


def get_movie_by_rank(rank, repo: AbstractRepository):

    movies = repo.get_movie_by_rank(target_rank=rank)

    movies_data = list()
    prev_rank = next_rank = None

    if len(movies) > 0:
        prev_rank = repo.get_rank_of_previous_movie(movies[0])
        next_rank = repo.get_rank_of_next_movie(movies[0])

        # Convert Articles to dictionary form.
        movies_data = movies_to_dict(movies)

    return movies_data, prev_rank, next_rank


def get_comments_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return comments_to_dict(movie.comments)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: 'Movie'):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'genres': movie.genres,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'year': movie.year,
        'duration': movie.duration,
        'rating': movie.rating,
        'votes': movie.votes,
        'revenue': movie.revenue,
        'metascore': movie.metascore,
        'comments': comments_to_dict(movie.comments)}
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(comment: Comment):
    comment_dict = {
        'username': comment.user.user_name,
        'article_id': comment.movie.rank,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]

