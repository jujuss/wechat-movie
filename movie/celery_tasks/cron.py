# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

from . import celery_app
from movie.weixin.sdk import push as daily_push
from movie.tool import media
from movie.tool import crawler
from movie import config

logger = logging.getLogger(__name__)


@celery_app.task(name='movie.cron.upload_resources_to_wx')
def celery_upload_resources_to_wx():
    try:
        media.push()
    except Exception, e:
        logger.exception(e)
        celery_app.current_task.retry(**config.CELERY_TASK_RETRY_CONFIG)


@celery_app.task(name='movie.cron.daily_push')
def celery_daily_push():
    try:
        daily_push.send_daily_push()
    except Exception, e:
        logger.exception(e)
        celery_app.current_task.retry(**config.CELERY_TASK_RETRY_CONFIG)


@celery_app.task(name='movie.cron.crawl')
def celery_crawl():
    try:
        spider = crawler.Crawler()
        spider.work()
    except Exception, e:
        logger.exception(e)
        celery_app.current_task.retry(**config.CELERY_TASK_RETRY_CONFIG)
