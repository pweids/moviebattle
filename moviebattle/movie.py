from dataclasses import dataclass
from typing import List

@dataclass
class Movie:
    url: str
    title: str
    genres: str
    directors: List[str]
    actors: List[str]
    date: str
    description: str
    mpaa_rating: str
    review_rating: float
    trailer: str
    viewed: bool

    def __hash__(self):
        return hash(self.url)

