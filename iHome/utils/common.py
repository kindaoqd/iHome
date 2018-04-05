# -*- coding: utf-8 -*-
from werkzeug.routing import BaseConverter
from functools import wraps
from flask import session, g, jsonify
from iHome.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_required(view_func):
    """登陆状态装饰器"""
    @wraps
    def wrapper(*args, **kwargs):
        if not 'user_id' in session:
            return jsonify(errno=RET.SESSIONERR, errmsg=u'用户未登录')
        else:
            g.user_id = session['user_id']
        return view_func(*args, **kwargs)
    return wrapper
