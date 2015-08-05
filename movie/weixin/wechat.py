# coding:utf-8

from flask import request, make_response
import hashlib
try:
    from xml.etree import cElementTree as ET # noqa
except:
    from xml.etree import ElementInclude as ET # noqa

from .. import app
from .. import config
from .msg import msg_text
from .msg import msg_event
from .msg import msg_voice


@app.route('/weixin', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    nonce = request.args.get('nonce', '')
    timestamp = request.args.get('timestamp', '')

    if check_signature(signature, nonce, timestamp):
        if request.method == 'GET':
            return make_response(request.args.get('echostr', ''))
        elif request.method == 'POST':
            app.logger.info(request.data)
            msg = parse_request_xml(request.data)
            msg_type = msg.get('MsgType')
            msg_cls = {
                "text": msg_text.TextMsg,
                'event': msg_event.EventMsg,
                'voice': msg_voice.VoiceMsg,
            }
            resp_msg = msg_cls[msg_type](msg).handle()
            app.logger.info(resp_msg)
            return make_response(resp_msg)
    else:
        return make_response('hello, weixin')


def check_signature(signature, nonce, timestamp):
    tmp_list = [config.token, timestamp, nonce]
    tmp_list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, tmp_list)
    hash_code = sha1.hexdigest()
    if hash_code == signature:
        return True
    else:
        return False


def parse_request_xml(xml_str):
    msg = dict()
    root = ET.fromstring(xml_str)
    if root.tag == 'xml':
        for child in root:
            msg[child.tag] = child.text
    return msg
