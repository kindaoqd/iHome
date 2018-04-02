# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from iHome.config import configs
from flask_wtf.csrf import CSRFProtect
from .utils.common import RegexConverter
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
redis_client = None


def set_logging(logging_level):
    # 设置日志的记录等级
    logging.basicConfig(level=logging_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 定义工厂函数，根据不同config_name创建不同配置的app
def get_app(config_name):
    set_logging(configs[config_name].LOGGING_LEVEL)
    app = Flask(__name__)  # 将app创建的目录即为工作目录
    # 加载配置
    app.config.from_object(configs[config_name])
    # 关联应用及session配置
    Session(app)
    # 关联应用开启csrf保护
    CSRFProtect(app)
    db.init_app(app)  # 数据库关联app方法 源码:flask_sqlalchemy\__init__.py 683
    global redis_client  # 全局变量redis数据库，注意在使用时再导入，以免无法导入
    redis_client = StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)
    # 添加自定义转换器
    app.url_map.converters['re'] = RegexConverter
    # 注册蓝图，为解决视图中有需要使用redis导入时异常
    from api_1_0 import api, verify_blue
    from .web_static import static_blue
    app.register_blueprint(api)
    app.register_blueprint(static_blue)
    app.register_blueprint(verify_blue)
    return app
