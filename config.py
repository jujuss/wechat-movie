# coding:utf8

# wexin config
token = 'ilovemovie'
appid = 'wxffaceb82ccad873e'
appsecret = 'e168947a5cf61520d2477535c4f7322d'
wx_access_token_uri = ('https://api.weixin.qq.com/cgi-bin/'
                       'token?grant_type=client_credential&appid=%s&secret=%s')
wx_upload_media_uri = ('https://api.weixin.qq.com/cgi-bin/media/'
                       'upload?access_token=%s&type=%s')
wx_upload_news_uri = ('https://api.weixin.qq.com/cgi-bin/media/'
                      'uploadnews?access_token=%s')
wx_mass_send_uri = ('https://api.weixin.qq.com/cgi-bin/message/mass/'
                    'send?access_token=%s')

# tuling config
tuling_robot_api = 'http://www.tuling123.com/openapi/api'
tuling_robot_key = '18c2dfecc0edad4a75d8f30f321857cf'

# crawler config
douban_url = 'http://movie.douban.com/nowplaying/shanghai/'
db_movie_info_uri = ('http://api.douban.com/v2/movie/subject/%s')

# server config
server_host = '0.0.0.0'
server_port = 8080

# server domain
server_domain = 'http://codemagic.tk'

# redis config
redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 1

# baidu_dev config
baidu_ak = '5aa13dd85f1ce1fab33ace6e9cb1be39'
baidu_map_geoconv_api = 'http://api.map.baidu.com/geoconv/v1/'
baidu_map_place_api = 'http://api.map.baidu.com/place/v2/search'
baidu_map_geocoding_api = 'http://api.map.baidu.com/geocoder/v2/'
baidu_map_radius = 5000
baidu_map_page_size = 5

# camera_pic list
cinema_pic_domain = 'http://7u2j19.com1.z0.glb.clouddn.com'
cinema_pics = \
    ['%s/%s_%d.jpg' % (cinema_pic_domain, 'cinema', x) for x in range(1, 21)]

# smtp config
mailhost = 'smtp.163.com'
fromaddr = 'qiuhunjihl@163.com'
toaddrs = ['steven_hl@163.com', 'chendannn@163.com']
credentials = ('qiuhunjihl@163.com', 'VoTfEpYHLA83iV')
subject = 'wechat_movie error'

# response_msg tpl
TextTpl = '''<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>'''

MultiTextTpl = '''<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%d</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>%d</ArticleCount>
                    <Articles>
                    %s
                    </Articles>
                    </xml>'''

MultiItemTpl = '''<item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>'''
