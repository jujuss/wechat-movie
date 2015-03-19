# coding:utf-8

from flask import make_response, request, redirect
from . import app

from libs import mcurl

@app.route('/movie/subject/<douban_id>/',methods=['GET','POST'])
@app.route('/movie/subject/<douban_id>',methods=['GET','POST'])
def show_douban(douban_id):
    # return mcurl.CurlHelper(mobile=True).get('http://movie.douban.com/subject/%s/'  % douban_id.encode('utf-8'))
    return redirect('http://movie.douban.com/subject/%s/' %  douban_id.encode('utf-8'))
