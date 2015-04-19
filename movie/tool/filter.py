# coding:utf-8

import redis
import time

from .. import config


def gen_now_top_movies(count=3):
    rconn = redis.Redis(host=config.redis_host, port=config.redis_port,
                        db=config.redis_db)
    now = time.strftime('%Y%m%d')
    now_movie_ids = \
        rconn.zrangebyscore("nowplaying", now, now)
    now_movies = list()
    for movie_id in now_movie_ids:
        movie = rconn.hgetall("now:movie:%s" % movie_id)
        movie['id'] = movie_id
        now_movies.append(movie)
    sorted_now_movies = sorted(now_movies, key=lambda x: x['score'],
                               reverse=True)
    now_top_movies = sorted_now_movies[:count]
    return now_top_movies
