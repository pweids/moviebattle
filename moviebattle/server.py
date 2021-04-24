from flask import Flask, render_template, jsonify, request, redirect
from moviebattle import app as mapp
import json, re
app = Flask(__name__)

tourney = None

articles = re.compile('^(an?|the)\s')
#sorter = lambda ms: sorted(ms, key=lambda m: articles.sub('', m.title.lower()))

@app.route('/')
def index():
    count = len(mapp.movies)
    genres = list(mapp.get_genres())
    genres.sort()

    global sorter
    sort = request.args.get('sort')
    if sort == 'date':
        sorter = lambda ms: sorted(ms, key=lambda m: m.date)
    elif sort == 'date-desc':
        sorter = lambda ms: sorted(ms, key=lambda m: m.date, reverse=True)
    else:
        sorter = lambda ms: sorted(ms, key=lambda m: articles.sub('', m.title.lower()))

    movies = list(mapp.movies)
    return render_template("index.html", count=count, movies=sorter(movies), genres=genres)


@app.route('/genre/<genre>')
def genres(genre=None):
    movies = mapp.get_movies_in_genre(genre)
    return render_template("genre.html", genre=genre, movies=movies)


@app.route('/add', methods=["POST"])
def add_movie():
    url = request.json['url']
    try:
        mapp.add_movie(url)
    except ValueError as e:
        return str(e), 400
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/random')
@app.route('/random/<v1>')
@app.route('/random/<v1>/<v2>')
def random_movie(v1=None, v2=None):
    if not v1:
        movies = mapp.get_random_movie()
    else:
        try:
            int(v1)
            movies = mapp.get_random_movie(genre=v2, count=int(v1))
        except ValueError:
            i = int(v2) if v2 else 1
            movies = mapp.get_random_movie(genre=v1, count=i)
    return jsonify(movies)


@app.route('/viewed/<url>')
def viewed(url):
    mapp.set_viewed(mapp.from_url(url))
    return redirect('/')


@app.route('/delete/<url>')
def delete(url):
    mapp.remove_movie(url)
    return redirect('/')


@app.route('/create_battle', methods=["POST"])
def start_battle():
    if 'count' in request.json:
        count = request.json['count']
        movies = list(mapp.get_random_movie(count=request.json['count']))
        print(count)
    else:
        urls = request.json['urls']
        if len(urls) <= 1:
            return redirect('/')
        movies = [mapp.from_url(url) for url in urls]
    global tourney
    tourney = mapp.Tournament(movies)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/battle')
def battle():
    if not tourney:
        return redirect('/')
    
    if tourney.get_winner():
        return redirect('/winner')

    matchup = tourney.get_current_matchup()
    return render_template('matchup.html', left=matchup[0], right=matchup[1])


@app.route('/set_winner/<url>')
def set_winner(url):
    movie = mapp.from_url(url)
    tourney.set_winner(movie)
    return redirect('/battle')


@app.route('/winner')
def winner():
    if not tourney:
        return redirect('/')
    w = tourney.get_winner()
    if not w:
        return redirect('/')
    
    return render_template('winner.html', movie=w)
