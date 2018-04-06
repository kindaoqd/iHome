# -*- coding: utf-8 -*-
from datetime import timedelta
from redis import StrictRedis
import logging


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
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=2)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    LOGGING_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    LOGGING_LEVEL = logging.DEBUG


class ProductConfig(Config):
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING


class UnitTestConfig(Config):
    LOGGING_LEVEL = logging.DEBUG

# 根据不同场景对应为不同配置类
configs = {
    'default': Config,
    'development': DevelopmentConfig,
    'product': ProductConfig,
    'UnitTest': UnitTestConfig
}

# constants
# 图片验证码Redis有效期， 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 短信验证码Redis有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 七牛空间域名
QINIU_DOMIN_PREFIX = "http://o91qujnqh.bkt.clouddn.com/"

# 城区信息redis缓存时间，单位：秒
AREA_INFO_REDIS_EXPIRES = 7200

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页显示条目数
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面Redis缓存时间，单位：秒
HOUSE_LIST_REDIS_EXPIRES = 7200

# 七牛云文件分布式存储
QINIU_ACCESS_KEY = 'yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW'
QINIU_SECRET_KEY = 'bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW'
QINIU_BUCKET_NAME = 'ihome'
