# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 15:46'


from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app
import os


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)


manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()