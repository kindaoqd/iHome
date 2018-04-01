# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from redis import StrictRedis
from flask_session import Session
from iHome.config import Config
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
# 加载配置
app.config.from_object(Config)
# 关联应用及session配置
Session(app)
# 关联应用开启csrf保护
CsrfProtect(app)
db = SQLAlchemy(app)
redis_client = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
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
