# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    """应用配置类"""
    # 调试设置
    DEBUG = True
    # 数据库关联配置
    SQLALCHEMY_DATABASE_URI = 'mysql://kinder:123@192.168.140.128:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 密钥设置
    SECRET_KEY = 'mgWj5NFlRvf8h2hGDJhSvzrR9VsxKfAF4Z6KorsK6gDOzhOAIstWcJEA9+JHj2CW'

app = Flask(__name__)
# 加载配置
app.config.from_object(Config)

db = SQLAlchemy(app)
# 构造migrate实例，关联app与db
Migrate(app, db)
# 创建迁移管理类实例并关联app
manager = Manager(app)
# 添加迁移命令并起别名‘db’
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    # app.run(debug=True)
    # 使用迁移管理器运行
    manager.run()
