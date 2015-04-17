# coding:utf-8

import logging
import logging.handlers


def _set_logger(logger):
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s['
                                  'line:%(lineno)d] %(levelname)s %(message)s',
                                  datefmt='%a, %d %b %Y %H:%M:%S')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

logger = logging.getLogger(__name__)
_set_logger(logger)
