# coding:utf-8

from flask import Flask

app = Flask(__name__)

from .weixin import wechat
import index
import movie
import navigate
