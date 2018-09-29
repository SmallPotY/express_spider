# coding=utf-8

import os


class Config(object):
    """基础配置类"""

    CSRF_ENABLED = True  # 激活跨站点请求伪造保护
    SECRET_KEY = '#$@!flk49FJ)djsd!@#**&fd@lf'  # 加密盐

    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static" + os.sep + "uploads" + os.sep)
    FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static" + os.sep + "uploads" + os.sep + "users" + os.sep)


class ProdConfig(Config):
    """生产模式"""
    pass


class DevConfig(Config):
    """开发模式"""
    DEBUG = True  # 调试模式

    # 数据库配置
    DIALECT = 'postgresql'
    DRIVER = 'psycopg2'
    USERNAME = 'smallpot'
    PASSWORD = 'yj'
    HOST = '58.63.214.44'
    PORT = '5432'
    DATABASE = 'express_spider'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configs = {
    'DevConfig': DevConfig,
    'ProdConfig': ProdConfig
}
