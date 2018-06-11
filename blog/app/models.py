from flask import current_app
from app.extensions import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin   # 记住用户的状态，类似于cookie和session
from datetime import datetime

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    # 头像
    icon = db.Column(db.String(40),default='default.jpg')

    # 添加博客的反向引用
    posts = db.relationship('Posts',backref = 'user',lazy = 'dynamic')
    # 添加收藏的反向引用
    favorites = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('不能访问密码属性')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    # 密码校验
    def vierify_password(self,password):
        return check_password_hash(self.password_hash,password)



    # 封装方法生成用于账户激活的token
    def generate_activate_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    # 校验激活的token
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)    # 判断是否有token这个值
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            return False
        # 如果用户没有激活
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
        return True

    # 校验找回密码的token
    @staticmethod
    def check_find_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 判断是否有token这个值
        except:
            return False
        u = User.query.get(data['id'])
        if u:
            return u

    # 封装修改邮箱的方法
    # 封装方法生成用于账户激活的token
    def generate_email_token(self,email,expires_in=3600):
        self.email = email
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id,'email':self.email})
    # 校验新邮箱
    @staticmethod
    def check_email_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)    # 判断是否有token这个值
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            return False
        # 如果用户没有激活
        if u:
            u.email = data['email']
            db.session.add(u)
        return True

    # 判断用户是否收藏指定模型
    def is_favorite(self,pid):
        # 所有收藏的博客
        favorite = self.favorites.filter(Posts.id==pid).first()
        if favorite:
            return True
        else:
            return False

    # 添加收藏
    def add_favorite(self,pid):
        p = Posts.query.get(pid)
        # favorite = self.favorites.all()
        # favorite.append(p)
        self.favorites.append(p)

    # 删除收藏
    def del_favorite(self,pid):
        p = Posts.query.get(pid)
        favorite = self.favorites.all()
        favorite.remove(p)


# 博客模型
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    rid = db.Column(db.Integer,index = True,default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    # 添加外键, 记录是谁发的
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))

# 用户收藏博客关联模型
collections = db.Table('collections',
                       db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                       db.Column('post_is', db.Integer,db.ForeignKey('posts.id'))
                       )




# 回调函数，当我们需要用到登录用户的信息时自动调用
@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


