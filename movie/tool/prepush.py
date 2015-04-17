#! /usr/bin/env python
# coding:utf-8
# 定时上传一些微信push的素材

import logging
import os.path as path
import config
import sys
import redis

from . import filter
from . import downloader
from ..lib import mcurl

logger = logging.getLogger(__name__)
root_path = path.abspath("../..")
curl = mcurl.CurlHelper()
rconn = redis.Redis(host=config.redis_host, port=config.redis_port,
                    db=config.redis_db)


def download_pics(movies):
    for movie in movies:
        movie_pic_url = movie['pic']
        pic_name = movie_pic_url.split('/')[-1]
        dest_path = root_path + "/%s" % pic_name

        if not path.exists(dest_path):
            ret = downloader.download(movie_pic_url, dest_path)
            if ret:
                logger.info('%s download complete', pic_name)
                movie['pic_abspath'] = dest_path


def get_access_token():
    # To Do 需要对access_token 做缓存处理
    access_token_api = config.wx_access_token_uri % \
        (config.appid, config.appsecret)
    res = curl.get(access_token_api, resp_type='json')
    if 'access_token' in res:
        return res['access_token']
    else:
        logger.error('Accquire access_token error, errcode: %s, errmsg: %s',
                     res['errcode'], res['errmsg'])
        return None


def upload_pics(access_token, files):
    upload_media_api = config.wx_upload_media_uri % \
        (access_token, 'thumb')
    mcurl.upload(upload_media_api, files)


def main():
    access_token = get_access_token()
    if access_token:
        logger.info('Get access_token error')
        sys.exit(-1)

    now_top_movies = filter.gen_now_top_movies()
    download_pics(now_top_movies)
    upload_file_infos = list()

    for movie in now_top_movies:
        upload_file_infos.append({"douban_id": movie['id'],
                                  "file_path": movie['pic_abspath'],
                                  "field": ""})

    ret = upload_pics(access_token, upload_file_infos)
    logger.info('Upload wx meida, get msg: %r', ret)

    # To Do
    # 需要将media_id写入数据库或者直接发送xinxi
    for info in ret:
        douban_id = info['douban_id']
        wx_media_id = info['wx_media_id']
        rconn.hset('now:movie:%s' % douban_id, 'wx_media_id', wx_media_id)
