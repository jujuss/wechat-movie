# coding:utf-8

import time
import redis
import random
import json

import config
from libs import mcurl

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
         else:
            return 'hello, world'

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
        elif event_key == 'M_LOCATION':
            return self._handle_click_location()

    def View(self):
        pass

    def Location(self):
        uid = self.redis.hget('wx:%s' % self.from_user, 'uid')
        loaction_lat = self.msg.get('Latitude','')
        location_long = self.msg.get('Longitude','')

        self.redis.hset('user:%d' % int(uid), 'latitude', loaction_lat)
        self.redis.hset('user:%d' % int(uid), 'longitude', location_long)

        return ('','')

    def _handle_click_location(self):
        uid = int(self.redis.hget('wx:%s' % self.from_user, 'uid'))
        curr_long = self.redis.hget('user:%d' % uid, 'longitude')
        curr_lat = self.redis.hget('user:%d' % uid, 'latitude')

        geoconv_url = '%s?ack=%s&coords=%s&output=%s' % (config.baidu_map_geoconv_api,config.baidu_ack,'%s,%s' %(curr_long,curr_lat), 'json')
        geoconv_res = json.loads(mcurl.CurlHelper().get(geoconv_url))

        if geoconv_res['status'] == 0:
            baidu_location = geoconv_res['result'][0]

        if baidu_location is not None:
            baidu_map_long = baidu_location['x']
            baidu_map_lat = baidu_location['y']

            return ('经度: %s, 纬度: %s' % (baidu_map_long, baidu_map_lat, ),'text')
        else:
            return ('为获取到用户地理位置信息，请重试','text')

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
