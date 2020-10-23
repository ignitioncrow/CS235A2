import csv

from Movie.domain.movie import Movie
from Movie.domain.actor import Actor
from Movie.domain.genre import Genre
from Movie.domain.director import Director

class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = []
        self.__dataset_of_directors = []
        self.__dataset_of_genres = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            for row in movie_file_reader:
                title = row['Title']
                description = str(row['Description'])
                year = int(row['Year'])
                duration = int(row['Runtime (Minutes)'])
                rating = float(row['Rating'])
                votes = int(row['Votes'])
                revenue = row['Revenue']
                metascore = row['Metascore']

                movie = Movie(title, description, year, duration, rating, votes, revenue, metascore)

                actors = row['Actors'].split(",")
                directors = Director(row['Director'])
                genres = row['Genre'].split(",")

                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.append(movie)

                if directors not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(directors)

                for a in actors:
                    actors = Actor(a)
                    if actors not in self.__dataset_of_actors:
                        self.__dataset_of_actors.append(actors)

                for g in genres:
                    genres = Genre(g)
                    if genres not in self.__dataset_of_genres:
                        self.__dataset_of_genres.append(genres)

    @property
    def dataset_of_movies(self) -> list:
        return self.__dataset_of_movies
    @property
    def dataset_of_actors(self) -> list:
        return self.__dataset_of_actors
    @property
    def dataset_of_directors(self) -> list:
        return self.__dataset_of_directors
    @property
    def dataset_of_genres(self) -> list:
        return self.__dataset_of_genres




