from nose.tools import *

from moviebattle import get_movie
from moviebattle.movie import Movie

ARRESTED_DEVELOPMENT = "https://www.imdb.com/title/tt0367279/"
BAD_WORDS = "https://www.imdb.com/title/tt2170299/"
NO_COUNTRY = "https://www.imdb.com/title/tt0477348/"

@raises(ValueError)
def test_bad_link():
    res = get_movie.scrape_data("https://www.imdb.com/name/hm0000867/")

def test_tv_link():
    res = get_movie.scrape_data(ARRESTED_DEVELOPMENT)

def test_good_link():
    res = get_movie.scrape_data(BAD_WORDS)
    assert 'name' in res and 'genre' in res

def test_get_bad_link():
    res = get_movie.get_movie("https://www.imdb.com/name/hm0000867/")
    assert isinstance(res, str)
    assert 'valid' in res

def test_get_tv():
    res = get_movie.get_movie(ARRESTED_DEVELOPMENT)
    assert isinstance(res, str)
    print(res)
    assert 'TV' in res

def test_get_movie():
    m = get_movie.get_movie(BAD_WORDS)
    assert isinstance(m, Movie)

def test_get_movie_2_dirs():
    m = get_movie.get_movie(NO_COUNTRY)
    assert len(m.directors) == 2
