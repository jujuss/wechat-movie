#! /usr/bin/env python
# coding:utf-8

from ...lib import mcurl
from ... import config
from ... import rconn


curl = mcurl.CurlHelper()


def get_access_token():
    if rconn.exists('wx:access_token'):
        return rconn.get('wx:access_token')
    access_token_api = config.wx_access_token_uri % \
        (config.appid, config.appsecret)
    res = curl.get(access_token_api, resp_type='json')
    if 'access_token' in res:
        access_token = res['access_token']
        expires_in = res['expires_in']
        rconn.set('wx:access_token', access_token, expires_in)
        return access_token
    else:
        raise IOError
