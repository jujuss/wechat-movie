# coding:utf-8

from flask import redirect
from .. import app


@app.route('/movie/subject/<douban_id>/', methods=['GET', 'POST'])
@app.route('/movie/subject/<douban_id>', methods=['GET', 'POST'])
def show_douban(douban_id):
    return redirect('http://movie.douban.com/subject/%s/mobile' %
                    douban_id.encode('utf-8'))
