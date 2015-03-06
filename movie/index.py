# coding:utf8

from movie import app

@app.route('/',methods=['GET','POST'])
def index():
    return 'hello,codemagic'
