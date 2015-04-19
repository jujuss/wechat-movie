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
    for info in ret:
        douban_id = info['douban_id']
        wx_media_id = info['wx_media_id']
        # rconn.hset('now:movie:%s' % douban_id, 'wx_media_id', wx_media_id)
        movie_info = rconn.hgetall('now:movie:%s' % douban_id)
        movie_info['pic_wx_media_id'] = wx_media_id
        rconn.zadd('push', douban_id, timestamp)
        rconn.hmset('push:%s:info' % douban_id, movie_info)
