
# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/22 16:45'

from flask import Blueprint,render_template,redirect,url_for,flash,request
from app.forms import PostsForm
from app.models import Posts
from flask_login import  current_user
from app.extensions import db

main = Blueprint('main',__name__)

@main.route('/',methods=['POST','GET'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            # 获取原始的用户对象
            u = current_user._get_current_object()
            # 创建对象
            p = Posts(content=form.content.data, user = u)
            # 保存到数据库
            db.session.add(p)
            flash('发表成功')
            return redirect(url_for('main.index'))
        else:
            flash('登录之后才可以发表')
            return redirect(url_for('user.login'))
    # 读取博客
    # posts = Posts.query.filter(Posts.id == 0)
    # 分页查询
    page = request.args.get('page', 1, int) # 将获取的页码参数转为int类型
    pagination = Posts.query.filter(Posts.rid==0).paginate(page,per_page=10,error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form = form, pagination = pagination, posts = posts)

