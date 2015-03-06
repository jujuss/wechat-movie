# coding:utf-8

from flask import request,make_response

from movie import app
import config
import hashlib
try:
    from xml.etree import cElementTree as ET
except:
    from xml.etree import ElementInclude as ET

@app.route('/weixin',methods = ['GET','POST'])
def wechat():
    signature = request.args.get('signature','')
    nonce = request.args.get('nonce','')
    timestamp = request.args.get('timestamp','')

    if checkSignature(signature,nonce,timestamp):
        if request.method == 'GET':
            return make_response(request.args.get('echostr',''))
        elif request.method == 'POST':
            app.logger.info(request.data)
            return make_response(request.data)
    else:
        return make_response('hello, weixin')


def checkSignature(signature,nonce,timestamp):
        tmp_list = [config.token,timestamp,nonce]
        tmp_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, tmp_list)
        hash_code = sha1.hexdigest()
        if hash_code== signature:
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

