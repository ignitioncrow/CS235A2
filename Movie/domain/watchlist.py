from Movie.domain.movie import Movie

class WatchList:
    def __init__(self):
        self.__movie_li = []
    def add_movie(self, movie:'Movie'):
        if isinstance(movie, Movie):
            if movie not in self.__movie_li:
                self.__movie_li.append(movie)
            else:
                pass
        else:
            raise TypeError
    def remove_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie):
            if movie in self.__movie_li:
                self.__movie_li.remove(movie)
            else:
                pass
        else:
            raise TypeError
    def select_movie_to_watch(self, index: int):
        if index >= 0 and index < len(self.__movie_li):
            return self.__movie_li[index]
        else:
            return None
    def size(self):
        return len(self.__movie_li)
    def first_movie_in_watchlist(self):
        if len(self.__movie_li) == 0:
            return None
        return self.__movie_li[0]
    def __iter__(self):
        self.__index = 0
        return self
    def __next__(self):
        if self.__index > self.size() - 1:
            raise StopIteration
        else:
            self.__index += 1
            return self.__movie_li[self.__index-1]



