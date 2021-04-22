from moviebattle import app
from moviebattle import movie


def test_get_random():
    app.add_movie('https://www.imdb.com/title/tt0482571')
    r = app.get_random_movie(genre="Drama")
    assert "Drama" in r[0].genres
    assert len(r) == 1

    r2 = app.get_random_movie(genre="Drama", count=2)
    assert all(["Drama" in m.genres for m in r2])
    assert len(r2) == 2

    r3 = app.get_random_movie(genre="None", count=2)
    assert len(r3) == 0


def test_from_url():
    app.add_movie('https://www.imdb.com/title/tt0477348')
    assert isinstance(app.from_url('tt0477348'), movie.Movie)