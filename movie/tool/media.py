#! /usr/bin/env python
# coding:utf-8
# 定时上传一些微信push的素材

import os
import os.path as path
import time

from .. import config
from .. import rconn
from .. import logger
from . import filter
from . import downloader
from ..lib import mcurl
from ..weixin.sdk.misc import get_access_token

curl = mcurl.CurlHelper()


def get_pic_path():
    root_path = path.dirname(__file__)
    root_path = path.dirname(path.dirname(root_path))
    return path.abspath(root_path) + "/download"


def get_abs_poster_path():
    root_path = path.dirname(__file__)
    root_path = path.dirname(path.dirname(root_path))

    return path.abspath(root_path) + "/movie/static/img/poster"


def download_pics(movies, pic_root_path):
    if not path.exists(pic_root_path):
        os.mkdir(pic_root_path)
    for movie in movies:
        movie_pic_url = movie['pic']
        pic_name = movie_pic_url.split('/')[-1]
        dest_path = pic_root_path + "/%s" % pic_name

        if not path.exists(dest_path):
            ret = downloader.download(movie_pic_url, dest_path)
            if ret:
                logger.info('%s download complete', pic_name)

        movie['pic_abspath'] = dest_path


def upload_pics(access_token, files):
    upload_media_api = config.wx_upload_media_uri % \
        (access_token, 'thumb')
    return curl.upload(upload_media_api, files)


def push():
    try:
        access_token = get_access_token()
    except IOError, e:
        logger.error('Get access_token error %r', e)
    try:
        pic_root_path = get_pic_path()
        logger.info('pic path: %r', pic_root_path)
        now_top_movies = filter.gen_now_top_movies()
        logger.info("Top movies: %r", now_top_movies)
        download_pics(now_top_movies, pic_root_path)
        upload_file_infos = list()

        for movie in now_top_movies:
            upload_file_infos.append({"douban_id": movie['id'],
                                      "file_path": movie['pic_abspath'],
                                      "field": ""})

        ret = upload_pics(access_token, upload_file_infos)
        logger.info('Upload wx meida, get msg: %r', ret)

        # 需要将media_id写入数据库
        timestamp = time.strftime('%Y%m%d')
        poster_path = get_abs_poster_path()
        if not path.exists(poster_path):
            os.mkdirs(poster_path)

        for info in ret:
            douban_id = info['douban_id']
            wx_media_id = info['wx_media_id']
            resp = \
                mcurl.CurlHelper().get(config.db_movie_info_uri % douban_id,
                                       resp_type='json')
            summary = resp['summary']
            img_small, img_medium, img_large = \
                resp['images']['small'], resp['images']['medium'],\
                resp['images']['large']

            img_large_name = img_large.split('/')[-1]
            img_large_dest_path = poster_path + "/%s" % img_large_name
            if not path.exists(img_large_dest_path):
                downloader.download(img_large, img_large_dest_path)
            img_large = \
                config.server_domain + \
                '/static/img/poster/%s' % img_large_name

            movie_info = rconn.hgetall('now:movie:%s' % douban_id)
            movie_info['summary'] = summary
            movie_info['img_small'] = img_small
            movie_info['img_medium'] = img_medium
            movie_info['img_large'] = img_large
            movie_info['pic_wx_media_id'] = wx_media_id
            rconn.zadd('push', douban_id, timestamp)
            rconn.hmset('push:%s:info' % douban_id, movie_info)
    except Exception as e:
        logger.error('Upload media error: %r', e)
