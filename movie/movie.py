# coding:utf-8

from flask import make_response,request
from . import app

from libs import mcurl

@app.route('/movie/subject/<douban_id>',methods=['GET','POST'])
def show_douban(douban_id):
    return mcurl.CurlHelper().get('http://movie.douban.com/subject/%s/'  % douban_id.encode('utf-8'))

