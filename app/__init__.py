# coding=utf-8
# -*- coding:utf-8 -*-
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import configs
from flask_moment import Moment



app = Flask(__name__)

app.config.from_object(configs['DevConfig'])
db = SQLAlchemy(app)
moment = Moment(app)
from app.express import express as express_buleprint

app.register_blueprint(express_buleprint)


# app.register_blueprint(admin_buleprint, url_prefix="/admin")  # 添加路由前缀


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
