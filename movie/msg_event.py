# coding:utf-8

import time
import redis
import random
import json

import config
from libs import mcurl
from . import app

class EventMsg(object):
    def __init__(self,msg):
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUserName")
        self.from_user = msg.get("FromUserName")
        self.redis = redis.Redis(host=config.redis_host,
                                 port=config.redis_port,
                                 db=config.redis_db)
        self.curl = mcurl.CurlHelper()


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
        uid = int(self.redis.hget('wx:%s' % self.from_user, 'uid'))
        loaction_lat = self.msg.get('Latitude','')
        location_long = self.msg.get('Longitude','')

        geoconv_url = '%s?ak=%s&coords=%s&output=%s' % (config.baidu_map_geoconv_api,config.baidu_ak,'%s,%s' %(location_long, loaction_lat), 'json')
        geoconv_res = json.loads(self.curl.get(geoconv_url))

        if geoconv_res['status'] == 0:
            baidu_location = geoconv_res['result'][0]
            self.redis.hset('user:%d' % uid, 'baidu_latitude', baidu_location.get('y',''))
            self.redis.hset('user:%d' % uid, 'baidu_longitude', baidu_location.get('x',''))
        else:
            self.redis.hset('user:%d' % uid, 'baidu_latitude', loaction_lat)
            self.redis.hset('user:%d' % uid, 'baidu_longitude', location_long)

        self.redis.hset('user:%d' % uid, 'latitude', loaction_lat)
        self.redis.hset('user:%d' % uid, 'longitude', location_long)

        return ('','')

    def _handle_click_location(self):
        uid = int(self.redis.hget('wx:%s' % self.from_user, 'uid'))
        baidu_map_long = self.redis.hget('user:%d' % uid, 'baidu_longitude')
        baidu_map_lat = self.redis.hget('user:%d' % uid, 'baidu_latitude')

        if baidu_map_long is None or baidu_map_lat is None:
            return ('定位失败，请打开GPS重新定位', 'text')
        else:
            place_search_url = '%s?ak=%s&query=%s&location=%s&radius=%d&output=%s&scope=%s&page_size=%d' % (config.baidu_map_place_api, config.baidu_ak, '电影院', '%s,%s' % (baidu_map_lat, baidu_map_long), config.baidu_map_radius, 'json', '2', config.baidu_map_page_size)
            app.logger.info(place_search_url)
            search_result = json.loads(self.curl.get(place_search_url))
    
            if search_result['status'] == 0:
                cinemas = search_result['results']
                res = []
                cinema_pic_urls = random.sample(config.cinema_pics, 5)
                index = 0
                for cinema in cinemas:
                    if cinema['detail_info'].has_key('detail_url'):
                        detail_url = cinema['detail_info']['detail_url']
                    else:
                        detail_url = '%s/navigate?start=%s&end=%s&end_name=%s' % (config.server_domain,
                            '%s,%s'%(baidu_map_long,baidu_map_lat),
                            '%s,%s'%(cinema['location']['lng'],cinema['location']['lat']),
                            cinema['address'])
    
                    res.append({'title': "%s" % ( cinema['name'],),
                                'description':'',
                                'picurl': cinema_pic_urls[index],
                                'url':detail_url})
                    index += 1
                return (res,'multitext')
            else:
                return ('经度: %s, 纬度: %s 未获取到周边信息' % (baidu_map_long, baidu_map_lat, ),'text')

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
