# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    """应用配置类"""
    # 调试设置
    DEBUG = True
    # 数据库关联配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 密钥设置
    SECRET_KEY = 'mgWj5NFlRvf8h2hGDJhSvzrR9VsxKfAF4Z6KorsK6gDOzhOAIstWcJEA9+JHj2CW'

app = Flask(__name__)
# 加载配置
app.config.from_object(Config)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    app.run(debug=True)
