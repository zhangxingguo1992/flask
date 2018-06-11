# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 16:47'

from .main import main
from .user import user
from .posts import posts

CONFIG_BLUEPRINT = (
    (main, ''),
    (user, '/user'),
    (posts,'/posts'),
)

def register_blueprint(app):
    for blueprint,url_prefix in CONFIG_BLUEPRINT:
        app.register_blueprint(blueprint,url_prefix = url_prefix)
