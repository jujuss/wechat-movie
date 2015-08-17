# coding:utf-8


import logging
import logging.handlers
import redis

from flask import Flask

from . import settings as config

app = Flask(__name__)


def _set_logger(logger):
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    sh = logging.handlers.SMTPHandler(config.mailhost, config.fromaddr,
                                      config.toaddrs, config.subject,
                                      config.credentials)
    sh.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s %(filename)s['
                                  'line:%(lineno)d] %(levelname)s %(message)s',
                                  datefmt='%a, %d %b %Y %H:%M:%S')
    ch.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(sh)

logger = logging.getLogger(__name__)
_set_logger(logger)

rconn = redis.Redis(host=config.redis_host, port=config.redis_port,
                    db=config.redis_db)

from . import index
from .weixin import wechat
from .movie import show, navigate

__all__ = ['index', 'show', 'navigate', 'wechat', 'config']
