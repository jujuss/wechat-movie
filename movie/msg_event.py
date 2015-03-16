# coding:utf-8

import config
import time
import redis
import random

class EventMsg(object):
    def __init__(self,msg):
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUserName")
        self.from_user = msg.get("FromUserName")
        self.redis = redis.Redis(host=config.redis_host,
                                 port=config.redis_port,
                                 db=config.redis_db)


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
         elif resp_msg_type == 'multitext':
            items = ''
            for content in resp_msg:
                items += config.MultiItemTpl % (content['title'],content['description'],content['picurl'],content['url'])
            return config.MultiTextTpl % (self.from_user, self.to_user, curr_timestamp, len(resp_msg), items)

    def Subscribe(self):
        # 用户注册
        uid = self.redis.incr('uid')
        self.redis.hset('user:%d' % uid, 'wx_openid', self.from_user)
        self.redis.hset('wx:%s' % self.from_user, 'uid', uid)
        return ('欢迎关注FindMe，在这里你可以找到最新最热的电影，祝你玩的愉快','text')

    def  UnSubscribe(self):
        return ('成功取消关注','text')

    def Scan(self):
        pass

    def Click(self):
        event_key = self.msg.get('EventKey','')
        if event_key == 'M_NOWPLAYING':
            return self._handle_click_nowplaying()
        elif event_key == 'M_UPCOMING':
            return self._handle_click_upcoming()

    def View(self):
        pass

    def Location(self):
        uid = self.redis.hget('wx:%s' % self.from_user, 'uid')
        loaction_lat = self.msg.get('Latitude','')
        location_long = self.msg.get('Longitude','')

        self.redis.hset('user:%d' % int(uid), 'latitude', loaction_lat)
        self.redis.hset('user:%d' % int(uid), 'longitude', location_long)

    def _handle_click_upcoming(self):
        curr_date = int(time.strftime('%Y%m%d'))
        movies = []
        for mid in self.redis.zrangebyscore("upcoming", curr_date, curr_date):
            minfo = self.redis.hgetall("coming:movie:%s" % mid)
            movies.append(minfo)

        res = []
        for movie in random.sample(movies, 3):
            res.append({"title": '%s %s上映' % (movie['title'],movie['release_date']), "description":"", "picurl": movie["pic"], "url": movie['description']})
        return (res,'multitext')

    def _handle_click_nowplaying(self):
        curr_date = int(time.strftime('%Y%m%d'))
        movies = []
        for mid in self.redis.zrangebyscore("nowplaying", curr_date, curr_date):
            minfo = self.redis.hgetall("now:movie:%s" % mid)
            movies.append(minfo)

        res = []
        for movie in random.sample(movies, 5):
            res.append({"title": '%s %s' % (movie['title'],movie['score']), "description":"", "picurl": movie["pic"], "url": movie['description']})
        return (res,'multitext')
