#! /usr/bin/env python
# coding: utf-8

import subprocess
import logging


logger = logging.getLogger(__name__)


def download(uri, destination=None):
    try:
        args = "wget -q %s " % uri
        if destination:
            args += "-O %s" % destination
        ret = subprocess.check_call(args, shell=True,
                                    stdout=open('/dev/null', 'w'),
                                    stderr=subprocess.STDOUT)
        if ret == 0:
            logger.info('Download %s complete', uri)
            return True
    except Exception, e:
        logger.info('Download exception %r', e)
        return False
