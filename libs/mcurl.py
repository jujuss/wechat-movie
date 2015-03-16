# coding:utf-8

import pycurl
import StringIO
import urllib

class CurlHelper(object):
    """CurlHelper"""
    def __init__(self, mobile=False):
        self.curl = pycurl.Curl()
        # self.curl.setopt(pycurl.VERBOSE, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 100)
        self.curl.setopt(pycurl.TIMEOUT, 1000)
        if mobile:
            self.curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4")
        else:
            self.curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36")
        self.curl.setopt(pycurl.REFERER, '')

    def get(self,url,params=None):
        if params:
            url = url % params
        self.curl.setopt(pycurl.URL, url)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        return res

    def post(self,url,params=None,data=""):
        if params:
            url = url % params
        self.curl.setopt(pycurl.URL, url.encode('utf-8')) #注意字符编码问题
        self.curl.setopt(pycurl.POSTFIELDS, data)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        return res

    def close(self):
        self.curl.close()
