# coding:utf-8

import config
import time
import redis

class EventMsg(object):
    def __init__(self,msg):
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUserName")
        self.from_user = msg.get("FromUserName")


    def handle(self):
         event_action = {
             "subscribe" : self.Subscribe,
             "unsubscribe": self.UnSubscribe,
             "SCAN" : self.Scan,
             "CLICK": self.Click,
             "VIEW": self.View,
             "LOCATION": self.Location,
         }

         resp_msg,resp_msg_type = event_action.get(self.event)()
         curr_timestamp = int(time.time())

         if resp_msg_type == 'text':
            return config.TextTpl % (self.from_user,self.to_user,curr_timestamp,resp_msg)

    def Subscribe(self):
        return ('欢迎关注FindMe，在这里你可以找到最新最热的电影，祝你玩的愉快','text')

    def  UnSubscribe(self):
        return ('成功取消关注','text')

    def Scan(self):
        pass

    def Click(self):
        event_key = self.msg.get('EventKey','')
        if event_key == 'M_NOWPLAYING':
            r_conn = redis.Redis(host=config.redis_host, port=config.redis_port, db=config.redis_db)
            curr_date = int(time.strftime('%Y%m%d'))
            for mid in r_conn.zrangebyscore("nowplaying", curr_date, curr_date):
                minfo = r_conn.hgetall("now:movie:%s" % mid)
                print minfo
        elif event_key == 'M_UPCOMING':
            pass

    def View(self):
        pass

    def Location(self):
        pass
