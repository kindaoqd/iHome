# -*- coding: utf-8 -*-
from datetime import timedelta
from redis import StrictRedis


class Config(object):
    """应用配置类"""
    # 调试设置
    DEBUG = True
    # 数据库关联配置
    SQLALCHEMY_DATABASE_URI = 'mysql://kinder:123@192.168.140.128:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 密钥设置
    SECRET_KEY = 'mgWj5NFlRvf8h2hGDJhSvzrR9VsxKfAF4Z6KorsK6gDOzhOAIstWcJEA9+JHj2CW'
    # 配置redis服务器
    REDIS_HOST = '192.168.140.128'
    REDIS_PORT = 6379
    # session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=4)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)


class DevelopmentConfig(Config):
    pass


class ProductConfig(Config):
    DEBUG = False


class UnitTestConfig(Config):
    pass


