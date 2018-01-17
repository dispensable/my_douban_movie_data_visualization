# -*- coding:utf-8 -*-

import re, os, json

from bottle import jinja2_view, route, run, static_file
from utils import MongoCon


@route('/', name="index")
@jinja2_view('index.html', template_lookup=['templates'])
def index():
    """
    {'name': {
        'score': '8.9'.
        'img_filename': 'test11111.jpg'
    }}
    """
    # 过滤对应类型的电影，并生成需要的数据
    movies_data = {}
    movies_to_show_re = re.compile(r".?恐怖.?")
    with MongoCon() as movie_db:
        movies_to_show = movie_db.find({"type": movies_to_show_re}).limit(80)
        
        for movie in movies_to_show:
            movies_data[movie['name']] = {}
            movies_data[movie['name']]['score'] = movie['score']
            movies_data[movie['name']]['img_filename'] = movie['img_filename']
    
    # score dict
    score_dict = {}
    for key, value in movies_data.items():
        score = str(value['score'])
        if not score_dict.get(score, ''):
            score_dict[score] = []
        score_dict[score].append({'name': key.replace("'", ''), 'img_filename': value['img_filename']})

    return {'movies_data': movies_data, 'score_dict': json.dumps(score_dict)}


@route('/poster_img/<filename>')
def send_img(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), 'poster_img'))


if __name__ == "__main__":
    run(port=8080, debug=True)