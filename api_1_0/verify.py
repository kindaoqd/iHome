# -*- coding: utf-8 -*-
from . import verify_blue
from flask import request, abort, make_response, jsonify
from iHome.utils.captcha.captcha import captcha
from iHome.utils.response_code import RET, error_map
from iHome import redis_client


@verify_blue.route('/verify_code')
def get_verify_code():
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')

    if not uuid:
        abort(RET.DATAERR, error_map[RET.DATAERR])

    # 调用验证码工具生成验证码图片
    name, text, image = captcha.generate_captcha()
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
        print e
        return jsonify(errno=RET.DATAERR, errmsg=error_map[RET.DATAERR])
    # 返回图片
    response = make_response(image)
    response.headers['Content_Type'] = 'image/jpg'  # 设定头信息
    return response
