'''
From an IMDB link, get the movie details
'''
from moviebattle.movie import Movie
import requests, bs4 # type: ignore
from PIL import Image

from typing import Union, Dict, List, Optional
import re
import json

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

IMDB_ID = str
id_re = re.compile(r'imdb\.com\/title\/(tt\d+)')

def get_tt(imdb_link) -> Optional[str]:
    matches: List[str] = id_re.findall(imdb_link)
    if not matches:
        return None
    return matches[0]


def scrape_data(imdb_link: IMDB_ID) -> Dict:
    url = get_tt(imdb_link)
    if not url:
        raise ValueError(f'"{imdb_link}" is not a valid IMDB movie title. Form should be "https://www.imdb.com/title/tt[numbers]"')

    resp: requests.Response = requests.get(imdb_link)
    soup = bs4.BeautifulSoup(resp.content, features='html.parser')
    script = soup.find('script', type='application/ld+json')
    data = json.loads(script.string)
    data['url'] = url
    return data


def save_compressed_image(img_url: str, movie_id: str) -> None:
    im = Image.open(requests.get(img_url, stream=True).raw)
    size = im.size
    size = (500, (500*size[1]) // size[0])
    im.resize(size).save(f'{dir_path}/static/images/{movie_id}.jpg', optimize=True, quality=85)


def fill_movie_from_imdb(data):
    m = {}
    m['url'] = data['url']
    m['title'] = data['name']
    m['genres'] = data['genre'] if isinstance(data['genre'], list) else [data['genre']]
    m['directors'] = [d['name'] for d in data['director']] if isinstance(data['director'], list) else [data['director']['name']]
    m['date'] = data['datePublished']
    m['description'] = data['description']
    m['mpaa_rating'] = data['contentRating']
    m['review_rating'] = float(data['aggregateRating']['ratingValue'])
    m['actors'] = [a['name'] for a in data['actor']]
    m['viewed'] = False

    save_compressed_image(data['image'], m['url'])

    return Movie(**m)


def get_movie(link: str) -> Union[Movie, str]:
    try:
        data : Dict = scrape_data(link)
        if data['@type'] != 'Movie':
            raise ValueError(f"Title is not a movie, but a {data['@type']}")
        return fill_movie_from_imdb(data)
    except ValueError as e:
        return str(e)
    except KeyError as e:
        return "Movie does not have enough data. Not made yet?"
    
	
