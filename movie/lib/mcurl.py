# coding:utf-8

import pycurl
import StringIO
import json

from .. import logger


class CurlHelper(object):

    """CurlHelper"""

    def __init__(self):
        self.curl = pycurl.Curl()
        # self.curl.setopt(pycurl.VERBOSE, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 100)
        self.curl.setopt(pycurl.TIMEOUT, 1000)
        self.curl.setopt(
            pycurl.USERAGENT, '''Mozilla/5.0 (Macintosh; Intel Mac OS X
                10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.
        0.2214.111 Safari/537.36''')

    def get(self, url, params=None, resp_type=None):
        if params:
            url = url % params
        if isinstance(url, unicode):
            url = url.encode('utf-8')
        self.curl.setopt(pycurl.URL, url)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        if resp_type == 'json':
            return json.loads(res)
        return res

    def post(self, url, params=None, data="", resp_type=''):
        if params:
            url = url % params
        if isinstance(url, unicode):
            url = url.encode('utf-8')
        self.curl.setopt(pycurl.URL, url.encode('utf-8'))  # 注意字符编码问题
        self.curl.setopt(pycurl.POSTFIELDS, data)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        if resp_type == 'json':
            return json.loads(res)
        return res

    def upload(self, url, files):
        '''专门用于微信批量上传素材的接口
        '''
        if isinstance(url, unicode):
            url = url.encode('utf-8')
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.POST, 1)

        res = list()
        try:
            for file_info in files:
                field = file_info['field']
                file_path = file_info['file_path']
                douban_id = file_info['douban_id']   # douban id
                self.curl.setopt(pycurl.HTTPPOST,
                                 [(field, (pycurl.FORM_FILE, file_path))])
                b = StringIO.StringIO()
                self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
                self.curl.perform()
                resp = json.loads(b.getvalue())
                b.close()

                if 'errcode' not in resp:
                    logger.info('upload success, %r', resp)
                    res.append({'douban_id': douban_id,
                                'wx_media_id': resp['thumb_media_id']})
                else:
                    logger.error('upload media error, %r', resp)
        except Exception, e:
            logger.error('upload error, %r', e)
        else:
            self.close()
            return res

    def close(self):
        self.curl.close()
