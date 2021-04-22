from moviebattle.movie import Movie
from moviebattle.get_movie import get_movie
from moviebattle.db import get_movies, save_movie, update_viewed

from sqlite3 import IntegrityError
from typing import Set, List, Tuple, Optional
from random import choices, shuffle
from copy import copy

movies: Set[Movie] = get_movies()


def add_movie(link: str):
    res = get_movie(link)
    if isinstance(res, str):
        raise ValueError(f"Error: Cannot add movie: {res}")
    else:
        save_movie(res)
        movies.add(res)
        

def get_random_movie(genre=None, count=1) -> List[Movie]:
    ms = list(get_movies_in_genre(genre))
    return choices(ms, k=count) if len(ms) >= count else ms


def get_genres() -> Set[str]:
    return {g for m in movies for g in m.genres}


def get_movies_in_genre(genre) -> Set[Movie]:
    return {m for m in movies if not genre or (genre.lower() in [g.lower() for g in m.genres])}


def get_viewed_movies() -> Set[Movie]:
    return {m for m in movies if m.viewed}


def get_unviewed_movies() -> Set[Movie]:
    return movies - get_viewed_movies()


def from_url(imdb_url: str) -> Optional[Movie]:
    for m in list(movies):
        if m.url == imdb_url:
            return m
    return None


def set_viewed(movie: Movie):
    movie.viewed = True
    update_viewed(movie)


Matchup = Tuple[Movie, Movie]

class Tournament:
    def __init__(self, candidates: List[Movie]):
        if len(candidates) <= 1:
            raise ValueError("Not enough candidates to start a tournament")
            
        self._next: List[Movie] = []
        self._curr: List[Matchup] = self._build_matches(copy(candidates))
        self._winner: Optional[Movie] = None
        self._curr_matchup: Optional[Matchup] = self._curr.pop()

    def get_winner(self) -> Optional[Movie]:
        return self._winner

    def get_current_matchup(self) -> Optional[Matchup]:
        return self._curr_matchup

    def set_winner(self, winner: Movie):
        matchup = self.get_current_matchup()
        if not matchup or winner not in matchup: return
        self._next.append(winner)

        try:
            self._curr_matchup = self._curr.pop()
        except IndexError:
            if len(self._next) == 1:
                self._winner = self._next.pop()
                self._curr_matchup = None
            else:
                tmp = copy(self._next)
                self._next = []
                self._curr = self._build_matches(tmp)
                self._curr_matchup = self._curr.pop()

    def _build_matches(self, ms: List[Movie]):
        shuffle(ms)
        n = len(ms) // 2
        self._next.extend(ms[2*n:])
        return list(zip(ms[0:n], ms[n:2*n]))
        