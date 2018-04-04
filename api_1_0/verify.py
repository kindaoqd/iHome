# -*- coding: utf-8 -*-
from . import api
from flask import request, abort, make_response, jsonify, current_app
from iHome.utils.captcha.captcha import captcha
from iHome.utils.response_code import RET, error_map
from iHome import redis_client, config
import logging, re, random
from iHome.utils.send_SMS import SendSMS


@api.route('/verify_code')
def get_verify_code():
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')

    if not uuid:
        abort(RET.DATAERR, error_map[RET.DATAERR])
    # 调用验证码工具生成验证码图片
    name, text, image = captcha.generate_captcha()
    logging.debug(u'图片验证码： '+text)
    current_app.logger.debug(u'图片验证码： '+text)
    # 拼接redis数据库key
    verify_code_key = 'verify_code:' + uuid
    # 使用redis_client保存验证码文本内容
    try:
        redis_client.set(verify_code_key, text)
        # 如果之前有记录通过last_uuid进行删除
        if last_uuid:
            # 拼接redis数据库key
            last_verify_code_key = 'verify_code:' + last_uuid
        # 使用redis_client删除
            redis_client.delete(last_verify_code_key, text)
    except Exception as e:
        # print e
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=error_map[RET.DATAERR])
    # 返回图片
    response = make_response(image)
    response.headers['Content_Type'] = 'image/jpg'  # 设定头信息
    return response


@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    uuid = request.json.get('uuid')
    mobile = request.json.get('mobile')
    verify_code = request.json.get('verify_code')

    if not all([uuid, mobile, verify_code]):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数传递不全')

    # 判断手机号是否合法
    try:
        verify_code_server = redis_client.get('verify_code:' + uuid)
    except Exception as e:
        logging.debug(e)
        current_app.logger.debug(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询图片验证码失败')

    if not verify_code_server:
        return jsonify(errno=RET.NODATA, errmsg=u'图片验证码不存在或已过期')

    # 比较服务器记录图片验证码。不区分大小写
    if verify_code.lower() != verify_code_server.lower():
        # 生成电话验证码
        return jsonify(errno=RET.PARAMERR, errmsg=u'图片验证码不正确')
    asms_code = '%06d' % random.randint(0, 999999)
    if SendSMS().send_template_sms(mobile, asms_code, config.SMS_CODE_REDIS_EXPIRES/60, '1'):
        return jsonify(errno=RET.THIRDERR, errmsg=u'短信验证码发送失败')
    try:
        redis_client.set('Mobile: '+mobile, asms_code)
    except Exception as e:
        logging.debug(e)
        current_app.logger.debug(e)
        return jsonify(errno=RET.DBERR, errmsg=u'储存短信验证码失败')
    return jsonify(errno=RET.OK, errmsg=u'短信验证码发送成功')
