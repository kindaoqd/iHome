# -*- coding: utf-8 -*-

from . import api
from flask import request, session, current_app, jsonify
from iHome.utils.response_code import RET
from iHome.models import User
import re
from iHome import redis_client, db


@api.route('/users', methods=['POST'])
def register():
    """注册用户 
    1. 获取参数 phone_code，mobile, password
    2. 校验参数完整性 手机合法性
    3. 使用mobile查询redis， 比较phone_code
    4. 查询数据库，确认mobile是否已注册
    5. 创建用户记录，保存数据库
    6. 默认登陆用户
    7. 返回响应
    """
    # 1. 获取参数 phone_code，mobile, password
    request_json_dict = request.json
    mobile = request_json_dict.get('mobile')
    phone_code = request_json_dict.get('phone_code')
    password = request_json_dict.get('password')
    # 2. 校验参数完整性 手机合法性
    if not all([mobile, phone_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数不完整')
    if not re.match(r'1[345678][0-9]{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机号格式不合法')
    # 3. 使用mobile查询redis， 比较phone_code
    try:
        phone_code_server = redis_client.get('Mobile:'+mobile)
        if not phone_code_server:
            return jsonify(errno=RET.NODATA, errmsg=u'手机验证码不存在')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'手机验证码查询失败')
    if phone_code_server != phone_code:
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机验证码不正确')
    # 4. 查询数据库，确认mobile是否已注册
    try:
        if User.query.filter(User.mobile == mobile).first():
            return jsonify(errno=RET.PARAMERR, errmsg=u'手机号已注册')
    except Exception as e:
        current_app.logger.debug(e)
    # 5. 创建用户记录，保存数据库
    try:
        user = User()
        user.mobile = mobile
        user.name = mobile
        user.password = password
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=u'用户保存数据库失败')
    # 6. 默认登陆用户
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    # 7. 返回响应
    return jsonify(errno=RET.OK, errmsg=u'注册成功')