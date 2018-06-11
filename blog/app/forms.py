# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 15:47'

from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import Length,EqualTo,Email,DataRequired
from flask_wtf.file import FileField,FileRequired,FileAllowed
from app.extensions import photos

# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[Length(2,20,'用户名必须在2-20字符之间')])
    password = PasswordField('密码',validators=[Length(3,12,'用户名必须在6-20字符之间')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password','两次密码不一致')])
    email = StringField('邮箱',validators=[Email('邮箱格式不正确')])
    submit = SubmitField('注册')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空')])
    password = PasswordField('密码',validators=[DataRequired("密码不能为空")])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


# 上传头像的表单
class UploadForm(FlaskForm):
    photo = FileField("头像",validators=[FileRequired('请选择文件'),FileAllowed(photos,message='只能图片')])
    submit = SubmitField('上传')

# 修改密码表单
class ChangeSecret(FlaskForm):
    oldkey = PasswordField('旧密码')
    newkey = PasswordField('新密码',validators=[Length(3,12,'密码必须在6—20字符之间')])
    confirm = PasswordField('确认密码',validators=[EqualTo('newkey','两次密码必须相同')])
    submit = SubmitField('确定修改')

# 找回密码
class FindmimaForm(FlaskForm):
    email = StringField('邮箱',validators=[Email('邮箱格式不对')])
    submit = SubmitField('发送邮箱验证')
class FindForm(FlaskForm):
    newkey = PasswordField('密码',validators=[Length(3,12,'3-12位')])
    confirm = PasswordField('确认密码',validators=[EqualTo('newkey','两次密码必须相同')])
    submit = SubmitField('确定修改')

# 修改邮箱
class ChangeEmail(FlaskForm):
    email = StringField('邮箱',validators=[Email('邮箱格式不对')])
    submit = SubmitField('确定修改')




# 发表博客表单
class PostsForm(FlaskForm):
    # 设置标签属性，可以使用render_kw设置
    content = TextAreaField('',render_kw={'placeholder':'这一刻的想法...'},validators=[Length(3,128,message='必须在3-128个字符之间')])
    submit = SubmitField('发表')

