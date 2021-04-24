from moviebattle.movie import Movie

from typing import Set, Tuple, Optional
from collections import namedtuple
import os
import sqlite3

MovieRow = namedtuple('MovieRow', 'url, title, genres, directors, actors, date,'
                      'description, mpaa_rating, review_rating, trailer, viewed')


DB_FILE = 'movies.db'
con: Optional[sqlite3.Connection] = None


def get_connection(db_file=None) -> sqlite3.Connection:
    global con
    global DB_FILE
    if not con or db_file != DB_FILE:
        DB_FILE = db_file or DB_FILE
        con = sqlite3.connect(DB_FILE)
        con.execute('''CREATE TABLE IF NOT EXISTS movies
                       (url TEXT PRIMARY KEY, title TEXT, genres TEXT, directors TEXT, actors TEXT,
                        date TEXT, description TEXT, mpaa_rating TEXT, review_rating REAL, trailer TEXT,
                        viewed INTEGER)''')
    return con


def _row_to_movie(row: MovieRow) -> Movie:
    tup = (row.url, row.title, row.genres.split(','), row.directors.split(','),
           row.actors.split(','), row.date, row.description, row.mpaa_rating,
           row.review_rating, row.trailer, bool(row.viewed))
    return Movie(*tup)


def _movie_to_row(movie: Movie) -> MovieRow:
    row = MovieRow(movie.url, movie.title, ','.join(movie.genres), ','.join(movie.directors),
        ','.join(movie.actors), movie.date, movie.description, movie.mpaa_rating,
        movie.review_rating, movie.trailer, int(movie.viewed))
    return row


def save_movie(movie: Movie, db_file=None):
    # make sure ID doesn't exist
    # save movie
    con = get_connection(db_file)
    with con:
        try:
            con.execute('''INSERT INTO movies(url, title, genres, directors, actors, date, 
                                description, mpaa_rating, review_rating, trailer, viewed)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', _movie_to_row(movie))
        except sqlite3.IntegrityError:
            print(f"Warning: {movie.title} already exists")


def update_viewed(movie: Movie, db_file=None):
    con = get_connection(db_file)
    with con:
        con.execute('''UPDATE movies
                       SET viewed = ?
                       WHERE url = ?''', 
                       (int(movie.viewed), movie.url))


def delete_movie(id: str, db_file=None):
    con = get_connection(db_file)
    with con:
        con.execute('DELETE FROM movies WHERE url=?', (id,))


def get_movies(db_file=None) -> Set[Movie]:
    con = get_connection(db_file)
    with con:
        cur = con.cursor()
        cur.execute('select * from movies')
        rows = cur.fetchall()
    return {_row_to_movie(MovieRow(*row)) for row in rows}
