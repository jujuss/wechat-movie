#! /usr/bin/env python
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
from bs4 import BeautifulSoup
import time
import threading


from ..lib import mcurl
from .. import config
from .. import rconn
from .. import logger


class Crawler(object):
    def __init__(self):
        try:
            self.redis = rconn
        except Exception as e:
            logger.error('error init crawler, exception: %r', e)


    def work(self):
        try:
            resp = mcurl.CurlHelper().get(config.douban_url)
            soup = BeautifulSoup(resp)
            t1 = threading.Thread(target=self.handle_nowplaying, args=(soup,))
            t2 = threading.Thread(target=self.handle_upcoming, args=(soup,))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception as e:
            logger.exception('error get movies info, exception: %r', e)

    def _filter_keywords(cls, movie):
        for keyword in config.keyworld_blacklists:
            if keyword in movie['data-title']:
                return True
        return False

    def handle_nowplaying(self, soup):
        try:
            nowplaying_node = soup.find_all('div', id='nowplaying')[0]
            curr_date = time.strftime('%Y%m%d')
            for m_node in \
                    nowplaying_node.find_all('li', id=re.compile(r'\d+')):
                if self._filter_keywords(m_node):
                    continue

                m_douban_id = m_node['id']
                m_title = m_node['data-title']
                m_score = m_node['data-score']
                m_description = config.server_domain + \
                    "/movie/subject/%s" % m_douban_id
                m_pic = m_node.find_all('img')[0]['src']

                self.redis.zadd('nowplaying', m_douban_id, int(curr_date))
                movie_info = {'title': m_title, 'score': m_score,
                              'description': m_description, 'pic': m_pic,
                              'summary': ''}
                self.redis.hmset('now:movie:%s' % m_douban_id, movie_info)
                logger.info('nowplaying: %s %s %s %s %s' %
                            (m_douban_id, m_title, m_score,
                             m_description, m_pic))
        except Exception as e:
            logger.error('handle_nowplaying error message: %r', e)

    def handle_upcoming(self, soup):
        try:
            upcoming_node = soup.find_all('div', id='upcoming')[0]
            curr_date = time.strftime('%Y%m%d')
            for m_node in upcoming_node.find_all('li', id=re.compile(r'\d+')):
                if self._filter_keywords(m_node):
                    continue

                m_douban_id = m_node['id']
                m_title = m_node['data-title']
                m_description = config.server_domain + \
                    '/movie/subject/%s' % m_douban_id
                m_pic = m_node.find_all('img')[0]['src']
                m_release_date = (m_node.find_all('li', 'release-date')[0]
                                  .stripped_strings.next())[:-2]
                self.redis.zadd('upcoming', m_douban_id, int(curr_date))
                movie_info = {'title': m_title,
                              'release_date': m_release_date,
                              'description': m_description, 'pic': m_pic,
                              'summary': ''}
                self.redis.hmset('coming:movie:%s' % m_douban_id, movie_info)
                logger.info('upcoming: %s %s %s %s %s' %
                            (m_douban_id, m_title, m_release_date,
                             m_description, m_pic))
        except Exception as e:
            logger.error('handle_upcoming error msg: %r' % e)


def main():
    spider = Crawler()
    spider.work()


if __name__ == '__main__':
    main()
