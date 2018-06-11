# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 15:48'

# 导入类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Message,Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class



# 创建对象
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
moment = Moment()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)

# 初始化
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)


    # 设置登录端点
    login_manager.login_view = 'user.login'
    # 设置提示信息
    login_manager.login_message = '登陆后才可以访问'



    # 初始化上传对象
    configure_uploads(app,photos)
    patch_request_class(app,size=None)