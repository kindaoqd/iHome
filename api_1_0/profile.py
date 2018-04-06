# -*- coding: utf-8 -*-
from . import api
from iHome.utils.common import login_required
from flask import g, current_app, jsonify, request, session
from iHome.models import User
from iHome.utils.storage import storage
from iHome.utils.response_code import RET
from iHome import config, db


@api.route('/users', methods=['GET'])
@login_required
def get_user_info():
    """用户信息"""
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')

    response_dict = user.to_dict()
    return jsonify(errno=RET.OK, errmsg='ok', data=response_dict)


@api.route('/users/avatar', methods=['POST'])
@login_required
def set_user_avatar():
    """设置用户头像"""
    user_id = g.user_id
    # 获取图像文件并read读取
    try:
        avatar = request.files.get('avatar').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=u'文件获取失败')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')
    # 调用工具函数上传图爿至七牛云，并记录文件key
    try:
        key = storage(avatar)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg=u'图片上传失败')
    # 保存数据库
    user.avatar_url = key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'数据保存失败')
    return jsonify(errno=RET.OK, errmsg=u'上传成功', data=config.QINIU_DOMIN_PREFIX+key)


@api.route('/users/name', methods=['POST'])
@login_required
def set_user_name():
    """设置用户名"""
    user_id = g.user_id
    new_name = request.json.get('name')
    if not new_name:
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数不完整')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')
    # 查询数据库确认用户名是否存在
    try:
        if User.query.filter(User.name == new_name).first():
            return jsonify(errno=RET.NODATA, errmsg=u'用户名已存在')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    # 保存数据库
    try:
        user.name = new_name
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'数据保存失败')
    # 更新session
    session['name'] = new_name
    return jsonify(errno=RET.OK, errmsg=u'上传成功')


@api.route('/users/auth', methods=['GET', 'POST'])
@login_required
def set_user_auth():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')
    if request.method == 'POST':
        request_json_dict = request.json
        real_name = request_json_dict.get('real_name')
        id_card = request_json_dict.get('id_card')
        if not all([real_name, id_card]):
            return jsonify(errno=RET.PARAMERR, errmsg=u'参数不完整')
        # 保存数据库
        user.real_name = real_name
        user.id_card = id_card
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=u'数据保存失败')
        return jsonify(errno=RET.OK, errmsg=u'认证成功')
    response_auth_dict = user.to_auth_dict()
    return jsonify(errno=RET.OK, errmsg='OK', data=response_auth_dict)
