# -*- coding: utf-8 -*-

from . import api
from flask import request, current_app, g, jsonify
from iHome import db
from iHome.utils.response_code import RET
from iHome.utils.common import login_required
from iHome.models import Order, House
from datetime import datetime


@api.route('/orders', methods=['POST'])
@login_required
def create_order():
    """创建订单"""
    user_id = g.user_id
    request_dict = request.json
    house_id = request_dict.get('house_id')
    sd = request_dict.get('start_date')
    ed = request_dict.get('end_date')
    if not all([house_id, sd, ed]):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数不完整')
    try:
        start_date = datetime.strptime(sd, '%Y-%m-%d')
        end_date = datetime.strptime(ed, '%Y-%m-%d')
        assert end_date > start_date, Exception(u'时间输入有误')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=u'时间格式有误')
    # 判断订房时间与订单中时间是否冲突及房屋是否存在
    try:
        conflict_orders = Order.query.filter(Order.house_id == house_id, start_date < Order.end_date,
                                             end_date > Order.begin_date).all()
        if conflict_orders:
            return jsonify(errno=RET.DATAEXIST, errmsg=u'房屋已被订')
        house = House.query.get(house_id)
        if not house:
            return jsonify(errno=RET.NODATA, errmsg=u'房屋不存在')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'数据库查询失败')
    # 新建并储存订单
    price = house.price
    days = (end_date - start_date).days
    new_order = Order()
    new_order.house_id = house_id
    new_order.user_id = user_id
    new_order.begin_date = start_date
    new_order.end_date = end_date
    new_order.house_price = price
    new_order.days = days
    new_order.amount = price * days
    try:
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=u'存储新订单失败')
    return jsonify(errno=RET.OK, errmsg='OK')


@api.route('/orders')
@login_required
def get_orders():
    """获取订单信息"""
    user_id = g.user_id
    role = request.args.get('role')
    if role not in ['custom', 'landlord']:
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数有误')
    try:
        if role == 'custom':
            orders = Order.query.filter(Order.user_id == user_id).all()
        else:
            orders = Order.query.filter(Order.house.user_id == user_id, Order.status == 'WAIT_ACCEPT').all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'')
    orders_list = []
    for order in orders:
        orders_list.append(order.to_dict())
    return jsonify(errno=RET.OK, errmsg='OK', data={'orders': orders_list})


@api.route('/orders/<int:order_id>/comment', methods=['PUT'])
@login_required
def set_comment(order_id):
    """评论"""
    user_id = g.user_id
    comment = request.json.get('comment')
    if not comment:
        return jsonify(errno=RET.PARAMERR, errmsg=u'无评内容')
    try:
        # 验证条件1.登录用户是否为订单用户 2.是否该订单号 3.订单状态是否为待评价
        order = Order.query.filter(Order.user_id == user_id, Order.id == order_id,
                                   Order.status == 'WAIT_COMMENT').first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'订单查询失败')
    # 更新评论及订单状态并保存
    order.comment = comment
    order.status = 'COMPLETE'
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=u'评论保存失败')
    return jsonify(errno=RET.OK, errmsg=u'评论成功')
