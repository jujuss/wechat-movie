# coding:utf-8

import time

from ... import config
from ... import app
from . import msg_robot


class VoiceMsg(object):

    def __init__(self, msg):
        self.msg = msg
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.content = msg.get('Recognition')
        if self.content:
            self.content = self.content.encode('utf-8')

    def handle(self):
        if self.content:
            resp_msg, resp_msg_type = \
                msg_robot.RobotMsg(self.from_user, self.content).get()
            curr_timestamp = int(time.time())
            app.logger.info('response msg: %r', resp_msg)
        else:
            resp_msg, resp_msg_type = '主人，您想要小的做什么呢?', 'text'

        if resp_msg_type == 'text':
            return config.TextTpl % (self.from_user, self.to_user,
                                     curr_timestamp, resp_msg)
        elif resp_msg_type == 'multitext':
            items = ''
            for content in resp_msg:
                items += config.MultiItemTpl % (
                    content['title'], content['description'],
                    content['picurl'], content['url'])
            return config.MultiTextTpl % (self.from_user, self.to_user,
                                          curr_timestamp, len(resp_msg), items)
