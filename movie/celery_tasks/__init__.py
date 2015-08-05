# -*- coding: utf-8 -*-

from __future__ import absolute_import


from celery import Celery
from movie import config


celery_app = Celery()
celery_app.config_from_object(config)

if __name__ == '__main__':
    celery_app.start()
