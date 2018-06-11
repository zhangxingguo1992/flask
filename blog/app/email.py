# -*- conding: utf-8 -*-
__author__ = 'zhangxg'
__data__ = '2018/5/23 13:17'
from app.extensions import mail
from flask import current_app,render_template
from flask_mail import Message
from threading import Thread


def async_send_mail(app,msg):
    # 邮件发送需要在程序上下文中进行,新的线程中没有上下文，需要手动创建
    with app.app_context():  # 创建上下文
        mail.send(msg)

# 封装函数发送邮件
def send_mail(subject,to,templates, **kwargs):
    # 从代理中获取代理的原始对象
    app = current_app._get_current_object()
    # 创建用于发送的邮件消息对象
    msg = Message(subject=subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    # 设置内容
    msg.html = render_template('email/'+templates, **kwargs)
    # 发送邮件
    # mail.send(msg)
    thr = Thread(target=async_send_mail, args=[app,msg])
    thr.start()
    return thr
