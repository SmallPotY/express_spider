# coding=utf-8
import uuid

from sqlalchemy import exists

from . import express
from flask import render_template, redirect, url_for, flash, session, request, abort, send_from_directory, jsonify
from app.express.forms import *
from app.models import Express
from functools import wraps
from app import db, app, moment
from app.express.forms import Serial_form
import time
import os
import datetime
from werkzeug.utils import secure_filename
from app.express.hepler import Excel


def change_filename(filename):
    fileinfo = os.path.join(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + '.' + fileinfo
    return filename



# 登陆状态验证装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('express.login', next=request.url))
            # pass
        return f(*args, **kwargs)

    return decorated_function



@express.route('/')
@user_login_req
def index():
    """首页"""
    return render_template('index.html')


@express.route('/express_list/')
@user_login_req
def express_list():
    """快递列表"""
    return render_template('express_list.html')


@express.route('/express_upload/', methods=['GET', 'POST'])
@user_login_req
def express_upload():
    """上传"""

    now = int(time.time())
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y%m%d%H%M%S", timeStruct)
    session['user'] = 'admin'
    serial_id = session.get('user') + strTime

    form = Serial_form()

    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)  # 获取后缀
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        form.url.data.save(app.config['UP_DIR'] + url)
        excel = Excel(app.config['UP_DIR'] + url)
        c = 0
        invalid = []
        for i in range(excel.max_row - 1):
            item = excel.next()
            s = Express(express_order=item[0], user_label=item[1], blong_user=session['user'])

            if not db.session.query(exists().where(Express.express_order == str(item[0]))).scalar():
                db.session.add(s)
            else:
                invalid.append(item[0])
            c += 1

        db.session.commit()

        rtext = ['导入结束，共计{}条记录,其中{}已存在未进行导入'.format(c, invalid), 'ok'] if invalid else ['导入结束，共计{}条记录'.format(c), 'err']
        flash(rtext[0], rtext[1])
        return redirect(url_for('express.express_upload'))

    return render_template('express_upload.html', serial_id=serial_id, form=form)


@express.route('/express_down/')
@user_login_req
def down_file():
    filepath = '模板.xlsx'
    return app.send_static_file(filepath)


@express.route('/api/express_data/')
@user_login_req
def express_data():
    q = Express.query.all()
    data = {"data": []}
    for i in q:
        # print(i.upload_time)

        temp = {
            "id": i.id,  # id
            "upload_time": i.upload_time,  # 上传时间
            "express_order": i.express_order,  # 单号
            "carriers": i.carriers,  # 承运商
            "user_label": i.user_label,  # 货物标签
            "took_time": i.took_time,  # 揽收时间
            "last_time": i.last_time,  # 最后更新时间
            "state": i.state,  # 快递状态
            "results": i.results,  # 查询结果
            "update_time": i.update_time,  # 信息更新时间
        }
        data['data'].append(temp)

    return jsonify(data)


@express.route('/login/', methods=['GET', 'POST'])
def login():
    """登陆"""
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        session['user'] = 'admin'
        return redirect(url_for('express.index'))
    return render_template('login.html', form=form)
