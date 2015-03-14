# coding:utf8

# wexin config
token = 'ilovemovie'
appid = 'wxffaceb82ccad873e'
appsecret = 'e168947a5cf61520d2477535c4f7322d'

# crawler config
douban_url = 'http://movie.douban.com/nowplaying/shanghai/'

# server config
server_host = '0.0.0.0'
server_port = 8080

# redis config
redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 1

# response_msg tpl
TextTpl = '''<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>'''
