from moviebattle import get_movie, db
from tempfile import TemporaryFile
import os

NO_COUNTRY = "https://www.imdb.com/title/tt0477348/"

def test_save_movie():
    dbf = 'test.db'
    try:
        m = get_movie.get_movie(NO_COUNTRY)
        db.save_movie(m, dbf)

        ms = db.get_movies(dbf)

        assert m in ms
    finally:
        os.remove(dbf)

def test_update():
    dbf = 'test2.db'
    try:
        m = get_movie.get_movie(NO_COUNTRY)
        db.save_movie(m, dbf)
        m.viewed = True
        db.update_viewed(m, dbf)
        
        ms = db.get_movies(dbf)

        assert m in ms
    finally:
        if os.path.exists(dbf):
            os.remove(dbf)