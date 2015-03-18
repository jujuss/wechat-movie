# coding:utf-8

from flask import render_template
from flask import request

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

from . import app
from libs import mcurl
import config


@app.route('/navigate')
def navigate():
    start_pos = request.args.get('start', '')
    end_pos = request.args.get('end', '')
    if start_pos and end_pos:
        start_pos_long, start_pos_lat = [float(i) for i in start_pos.split(',')]
        end_pos_long, end_pos_lat = [float(i) for i in end_pos.split(',')]
        end_name = request.args.get('end_name')
        baidu_geocoding_url = '%s?ak=%s&location=%s&output=%s' % (config.baidu_map_geocoding_api, config.baidu_ak, '%s,%s'%(start_pos_lat,start_pos_long), 'json')
        curr_pos_info = json.loads(mcurl.CurlHelper().get(baidu_geocoding_url))
        app.logger.info(curr_pos_info)
        if curr_pos_info['status'] == 0:
            start_name = curr_pos_info['result'].get('formatted_address', '我的位置')
            region_name = curr_pos_info['result']['addressComponent']['city']
        else:
            start_name = '我的位置'
            region_name = '上海'
        kwargs = {'start_long': start_pos_long, 'start_lat': start_pos_lat,
                  'end_long': end_pos_long, 'end_lat': end_pos_lat,
                  'start_name': start_name, 'end_name': end_name,
                  'region_name': region_name}
        return render_template('navigate.html', **kwargs)
    else:
        return render_template('index.html', content='您提供的地理位置不正确，请重新输入!')
