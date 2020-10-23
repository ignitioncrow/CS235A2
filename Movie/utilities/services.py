from typing import Iterable
import random

from Movie.adapters.repository import AbstractRepository
from Movie.domain.movie import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]
    return genre_names


def get_random_movie(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movie_by_rank(random_ids)

    return movie_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.id,
        'title': movie.title,
        'release_yr': movie.release_year,
        'runtime': movie.runtime_minutes,
        'description': movie.description,
        'genres': movie.genres,
        'actors': movie.actors,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
