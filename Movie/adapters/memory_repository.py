import csv
import os
from datetime import datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from Movie.adapters.repository import AbstractRepository, RepositoryException
from Movie.domain.actor import Actor
from Movie.domain.director import Director
from Movie.domain.genre import Genre
from Movie.domain.movie import Movie
from Movie.domain.user import User
from Movie.domain.comment import Comment, make_comment


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__movies = list()
        self.__actors = list()
        self.__directors = list()
        self.__users = list()
        self.__comments = list()
        self.__genres = list()
        self.__movie_index = dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self.__movies, movie)
        #self.__movies.append(movie)
        self.__movie_index[movie.rank] = movie

    def get_movie(self, rank: int) -> Movie:
        movie_to_return = None
        try:
            movie_to_return = self.__movie_index[rank]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie_to_return

    def get_movies(self) -> List[Movie]:
        return self.__movies

    def get_movie_by_rank(self, target_rank: int) -> List[Movie]:
        target_movie = Movie(
            rank=target_rank,
            title=None,
            description=None,
            year=None,
            duration=None,
            rating=None,
            votes=None,
            revenue=None,
            metascore=None
        )
        matching_movies = list()
        try:
            """
            movie = self.__movies[target_rank]
            target_movie.append(movie)"""
            rank = self.movie_index(target_movie)
            for movie in self.__movies[rank:None]:
                if movie.rank == target_rank:
                    matching_movies.append(movie)
                else:
                    break
        except IndexError or KeyError or ValueError:
            pass

        return matching_movies

    def get_number_of_movies(self):
        return len(self.__movies)

    def get_first_movie(self):
        if len(self.__movies) > 0:
            return self.__movies[0]

    def get_last_movie(self):
        if len(self.__movies) > 0:
            return self.__movies[-1]

    def get_movie_by_genre(self, genre: Genre):
        movie_genre_li = []
        for mov in self.__movies:
            if isinstance(genre, Genre):
                if genre in mov.genres:
                    movie_genre_li.append(mov)
                else:
                    pass
            else:
                break
        return movie_genre_li

    def get_movie_by_actor(self, actor: Actor):
        movie_actor_li = []
        for mov in self.__movies:
            if isinstance(actor, Actor):
                if actor in mov.actors:
                    movie_actor_li.append(mov)
                else:
                    pass
            else:
                break
        return movie_actor_li

    def get_movie_by_director(self, director: Director):
        movie_director_li = []
        for mov in self.__movies:
            if isinstance(director, Director):
                if director == mov.director():
                    movie_director_li.append(mov)
                else:
                    pass
            else:
                break
        return movie_director_li

    def get_rank_of_previous_movie(self, movie: Movie):
        previous_rank = None

        try:
            index = movie.rank
            for stored_movie in reversed(self.__movies[0:index]):
                if stored_movie.rank < movie.rank:
                    previous_rank = stored_movie.rank
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_rank

    def get_rank_of_next_movie(self, movie: Movie):
        next_rank = None

        try:
            index = movie.rank
            for stored_movie in self.__movies[index+1:len(self.__movies)]:
                if stored_movie.rank > movie.rank:
                    next_rank = stored_movie.rank
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_rank

    def add_actor(self, actor: Actor):
        self.__actors.append(actor)

    def get_actor(self) -> List[Actor]:
        return self.__actors

    def add_director(self, director: Director):
        if director not in self.__directors and isinstance(director, Director):
            self.__directors.append(director)

    def get_director(self):
        return self.__directors

    def get_genre(self) -> List[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        if genre not in self.__genres and isinstance(genre, Genre):
            self.__genres.append(genre)

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        self.__comments.append(comment)

    def get_comments(self):
        return self.__comments

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self.__movies, movie)
        if index != len(self.__movies) and self.__movies[index].rank == movie.rank:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        movie_file_reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(movie_file_reader)

        # Read remaining rows from the CSV file.
        for row in movie_file_reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    for row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        title = str(row[1])
        year = int(row[6])
        actors = row[5].split(",")
        directors = Director(row[4])
        genres = row[2].split(",")
        description = str(row[3])
        ranking = int(row[0])
        duration = int(row[7])
        ratings = float(row[8])
        votes = int(row[9])
        metascore = row[11]
        revenue = row[10]

        movie = Movie(rank=ranking,
                      title=title,
                      description=description,
                      year=year,
                      duration=duration,
                      rating=ratings,
                      votes=votes,
                      revenue=revenue,
                      metascore=metascore
                      )
        repo.add_movie(movie)
        # add directors
        repo.add_director(directors)
        movie.director = directors

        # add actors to movies and repo
        for a in actors:
            actor = Actor(a)
            repo.add_actor(actor)
            movie.add_actor(actor)

        # add genres to movies and repo
        for g in genres:
            genre = Genre(g)
            repo.add_genre(genre)
            movie.add_genre(genre)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies(data_path, repo)
    users = load_users(data_path, repo)
    load_comments(data_path, repo, users)
