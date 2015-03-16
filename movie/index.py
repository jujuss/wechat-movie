# coding:utf8

from . import app

@app.route('/',methods=['GET','POST'])
def index():
    return 'hello,codemagic'
