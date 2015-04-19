#! /usr/bin/env python
# coding:utf-8

import time
import json

from . import misc
from ... import config
from ... import logger
from ... import rconn
from ...lib import mcurl

curl = mcurl.CurlHelper()


def gen_push_news():
    timestamp = time.strftime('%Y%m%d')
    push_ids = rconn.zrangebyscore('push', timestamp, timestamp)
    articles = list()
    for push_id in push_ids:
        push_info = rconn.hgetall('push:%s:info' % push_id)
        article = {"thumb_media_id": push_info['pic_wx_media_id'],
                   "author": "",
                   "title": "%s %s" % (push_info['title'], push_info['score']),
                   "content_source_url": push_info['description'],
                   "content": push_info['title'],
                   "digest": "",
                   "show_cover_pic": "0"}
        articles.append(article)
    msg = json.dumps({"articles": articles})
    return msg


def mget_openid():
    max_uid = int(rconn.get('uid'))
    wx_openids = list()
    for uid in xrange(1, max_uid + 1):
        wx_openid = rconn.hget('user:%s' % uid, 'wx_openid')
        wx_openids.append(wx_openid)

    return wx_openids


def send_job():
    try:
        access_token = misc.get_access_token()
        news = gen_push_news()
        wx_openids = mget_openid()
        logger.info('news: %r', news)
        logger.info('wx_openids: %r', wx_openids)
        resp = curl.post(config.wx_upload_news_uri % access_token, data=news,
                         resp_type='json')
        logger.info('upload news, get response: %r', resp)
        if 'media_id' in resp:
            news_media_id = resp['media_id']
            send_req_data = {"touser": wx_openids,
                             "mpnews": {"media_id": news_media_id},
                             "msgtype": "mpnews"}
            send_req_data = json.dumps(send_req_data)
            logger.info('send_req_data: %r', send_req_data)
            res = curl.post(config.wx_mass_send_uri % access_token,
                            data=send_req_data, resp_type='json')
            logger.info('push job, get msg: %r', res)
            if 'msg_id' in res:
                rconn. hset("%s:job" % time.strftime('%Y%m%d'), 'msg_id',
                            res['msg_id'])
            else:
                logger.error('push job error, errcode:%s errmsg:%s',
                             res['errcode'], res['errmsg'])
        else:
            logger.info('upload news error, errcode:%s errmsg:%s',
                        resp['errcode'], resp['errmsg'])
    except IOError, e:
        logger.error('Get access_token error %r', e)
