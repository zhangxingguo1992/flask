# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 16:50'


from flask import  Blueprint,render_template,flash,url_for,redirect,current_app,request
from app.forms import FindForm,ChangeEmail
from app.forms import RegisterForm,LoginForm,UploadForm,ChangeSecret,FindmimaForm
from app.email import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models import User
from app.extensions import db,photos
from flask_login import login_user,current_user,logout_user,login_required
import os
from PIL import Image

user = Blueprint('user', __name__)

# 用户注册
@user.route('/register/',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据提交的数据创建用户对象
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        # 保存到数据库中
        db.session.add(u)
        # 手动提交，此时需要用到用户的id
        db.session.commit()
        # 发送激活邮件
        token = u.generate_activate_token()
        send_mail('账户激活',form.email.data,'activate.html',username = form.username.data,token=token)
        # 发送提示
        flash('注册成功，请点击邮件连接完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html',form=form)


# 用户激活
@user.route('/activate/<token>/')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))



@user.route('/login/',methods = ['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u= User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash("账户未激活，请激活后登录")
        elif u.vierify_password(form.password.data):
            # 用户登录，顺便完成记住我的操作
            login_user(u,remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码不对')
    return render_template('user/login.html',form=form)



@user.route('/logout/')
def logout():
    # 退出登录。销毁session
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

# 路由保护，只有登录状态才可以访问
@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')

def random_string(length=16):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))

@user.route('/icon/',methods=['POST','GET'])
def icon():
    form = UploadForm()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.photo.data.filename)[1]
        # 生成随机文件名
        filename = random_string() + suffix
        photos.save(form.photo.data,name=filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(pathname)
        # 重新设置尺寸
        img.thumbnail((64, 64))
        # 保存图片
        img.save(pathname)
        # 删除原来的投降文件,不是默认的头像才删除
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        current_user.icon = filename
        db.session.add(current_user)
    img_url = url_for('static', filename = 'upload/' + current_user.icon)
    return render_template('user/icon.html',form = form ,img_url = img_url)


# 修改密码
@user.route('/mima/',methods=['POST','GET'])
def mima():
    form = ChangeSecret()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        if u.vierify_password(form.oldkey.data):
            u.password = form.newkey.data
            db.session.add(u)
            flash('修改密码成功')
            return redirect(url_for('user.login'))
        else:
            flash('原始密码不对')
    return render_template('user/mima.html',form = form )
# 找回密码：
@user.route('/find/',methods = ['POST','GET'])
def find():
    form = FindmimaForm()
    if form.validate_on_submit():
        u = User.query.filter(User.email==form.email.data).first()
        if u:
            token = u.generate_activate_token()
            send_mail('确认修改密码', form.email.data, 'findmima.html', token=token)
            # 如果邮件激活了
            return redirect(url_for('user.change',token=token))
        else:
            flash('没有该用户')
    return render_template('user/findmima.html', form=form)

@user.route('/change/<token>/',methods=['POST','GET'])
def change(token):
    form = FindForm()
    if form.validate_on_submit():
        if User.check_find_token(token):
            u = User.check_find_token(token)
            u.password = form.newkey.data
            db.session.add(u)
            flash('修改密码成功')
            return redirect(url_for('user.login'))
        else:
            flash('修改失败')
    return render_template('user/find.html',form = form)


# 修改邮箱
@user.route('/changeemail/',methods = ['POST','GET'])
def changeemail():
    form = ChangeEmail()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        token = u.generate_email_token(form.email.data)
        send_mail('修改邮箱',form.email.data,'xiugaiemail.html',token = token)
        flash('申请提交成功，去邮箱激活修改')
        return redirect(url_for('main.index'))
    return render_template('email/changeemail.html',form = form)
# 激活邮箱
@user.route('/newemail/<token>/',methods=['POST','GET'])
def newemail(token):
    if User.check_email_token(token):
        flash('修改成功')
        return redirect(url_for('main.index'))
    else:
        flash('修改失败')
        return redirect(url_for('main.index'))