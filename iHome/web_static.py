# -*- coding: utf-8 -*-
from flask import Blueprint, current_app

static_blue = Blueprint('web_static', __name__)


@static_blue.route('/<re(".*"):file_name>')
def get_static(file_name):
    # 需求1：http://127.0.0.1:5000/login.html
    # 需求2：http://127.0.0.1:5000/ 默认加载index.html
    # 需求3：http://127.0.0.1:5000/favicon.ico  加载title图标
    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name
    return current_app.send_static_file(file_name)
