# coding:utf-8

import logging
import logging.handlers

import config


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
