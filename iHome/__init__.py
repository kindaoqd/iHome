# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from iHome.config import configs
from flask_wtf.csrf import CSRFProtect
from .utils.common import RegexConverter

db = SQLAlchemy()
redis_client = None


# 定义工厂函数，根据不同config_name创建不同配置的app
def get_app(config_name):
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
