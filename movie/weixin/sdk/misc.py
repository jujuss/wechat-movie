#! /usr/bin/env python
# coding:utf-8

from ...lib import mcurl
import config

curl = mcurl.CurlHelper()

def get_access_token():
    # To Do 需要对access_token 做缓存处理
    access_token_api = config.wx_access_token_uri % \
        (config.appid, config.appsecret)
    res = curl.get(access_token_api, resp_type='json')
    if 'access_token' in res:
        return res['access_token']
    else:
        raise IOError
