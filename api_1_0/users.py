# -*- coding: utf-8 -*-
from . import api
from iHome.utils.common import login_required
from flask import g, current_app, jsonify, request
from iHome.models import User
from iHome.utils.response_code import RET
from qiniu.services.storage.uploader import put_file
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

    data = {
        'name': user.name,
        'mobile': user.mobile,
        'avatar_url': config.QINIU_DOMIN_PREFIX+user.avatar_url
    }
    return jsonify(errno=RET.OK, errmsg='ok', data=data)


@api.route('/users/avatar', methods=['POST'])
@login_required
def set_user_avatar():
    """设置用户头像"""
    user_id = g.user_id
    # 获取图像文件
    avatar = request.files.get('avatar')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')
    # 上传图爿至七牛云，并记录文件key
    try:
        key = put_file(config.QINIU_UP_TOKEN, config.QINIU_KEY, avatar)
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


@api.route('/users/auth', methods=['GET', 'POST'])
@login_required
def set_user_auth():
    user_id = g.user_id
    request_dict = request.json
    real_name = request_dict.get('real_name')
    id_card = request_dict.get('id_card')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg=u'用户不存在')
    # 保存数据库
    user.real_name = real_name
    user.id_card = id_card
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'数据保存失败')
    return jsonify(errno=RET.OK, errmsg=u'认证成功')
