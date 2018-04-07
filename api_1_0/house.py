# -*- coding: utf-8 -*-
from . import api
from iHome.models import Area, Facility, House, HouseImage, Order
from flask import current_app, jsonify, request, g, session
from iHome.utils.response_code import RET
from iHome.utils.common import login_required
from iHome.utils.storage import storage
from iHome import redis_client, db, config
from datetime import datetime


@api.route('/areas')
def get_areas_info():
    """获取地区信息"""
    # 查询缓存，使用eval将字符串数据转换成对象数据
    try:
        areas_list = eval(redis_client.get('Areas'))
        if areas_list:
            return jsonify(errno=RET.OK, errmsg='OK', data=areas_list)
    except Exception as e:
        current_app.logger.error(e)
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询地区数据失败')
    # 拼接字典列表返回数据
    areas_list = []
    for area in areas:
        areas_list.append(area.to_dict())
    # 记录缓存数据
    try:
        redis_client.set('Areas', areas_list, config.HOME_PAGE_DATA_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
    return jsonify(errno=RET.OK, errmsg='OK', data=areas_list)


@api.route('/houses', methods=['POST'])
@login_required
def pub_house():
    """发布房源"""
    user_id = g.user_id
    request_json_dict = request.json
    title = request_json_dict.get('title')
    price = request_json_dict.get('price')
    area_id = request_json_dict.get('area_id')
    address = request_json_dict.get('address')
    room_count = request_json_dict.get('room_count')
    acreage = request_json_dict.get('acreage')
    unit = request_json_dict.get('unit')
    capacity = request_json_dict.get('capacity')
    beds = request_json_dict.get('beds')
    deposit = request_json_dict.get('deposit')
    min_days = request_json_dict.get('min_days')
    max_days = request_json_dict.get('max_days')
    facility = request_json_dict.get('facility')

    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days, facility]):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数不完整')

    # 查询facility对象
    try:
        facility_items = Facility.query.filter(Facility.id.in_(facility)).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询配置失败')
    # 记录数据库
    new_house = House()
    new_house.user_id = user_id
    new_house.title = title
    new_house.price = float(price)*100
    new_house.area_id = area_id
    new_house.address = address
    new_house.room_count = room_count
    new_house.acreage = acreage
    new_house.unit = unit
    new_house.capacity = capacity
    new_house.beds = beds
    new_house.deposit = float(deposit)*100
    new_house.min_days = min_days
    new_house.facilities = facility_items
    try:
        db.session.add(new_house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=u'新房屋保存数据库失败')
    return jsonify(errno=RET.OK, errmsg='ok', data={'house_id': new_house.id})


@api.route('/houses/<int:house_id>/images', methods=['POST'])
@login_required
def upload_house_image(house_id):
    """上传房屋图片"""
    try:
        image = request.files.get('house_image').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=u'获取图片文件异常')
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'房屋查询异常')
    if not house:
        return jsonify(errno=RET.PARAMERR, errmsg=u'房屋不存在')
    # 图片上传七牛云，记录key
    try:
        image_key = storage(image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg=u'图片上传失败')
    house_image = HouseImage()
    house_image.url = image_key
    house_image.house_id = house_id
    house.index_image_url = image_key
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg=u'数据库保存失败')
    return jsonify(errno=RET.OK, errmsg='OK', data={'url': config.QINIU_DOMIN_PREFIX+image_key})


@api.route('/houses/detail/<int:house_id>')
def house_detail(house_id):
    """房屋详情信息"""
    user_id = session.get('user_id', -1)
    try:
       house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'房屋查询异常')
    if not house:
        return jsonify(errno=RET.NODATA, errmsg=u'房屋不存在')

    house_dict = house.to_full_dict()
    return jsonify(errno=RET.OK, errmsg='OK', data={'house': house_dict, 'user_id': user_id})


@api.route('/houses/index')
def house_index():
    """房屋首页"""
    try:
        houses = House.query.order_by(House.create_time).limit(config.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'房屋查询失败')
    house_list = []
    for house in houses:
        house_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg='OK', data=house_list)


@api.route('/houses')
def get_house_list():
    """获取房屋列表信息"""
    # url:http://127.0.0.1:5000/search.html?aid=1&aname=&sd=&ed=
    aid = request.args.get('aid')
    sk = request.args.get('sk')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    start_date = None
    end_date = None
    try:
        if sd:
            start_date = datetime.strptime(sd, '%Y-%m-%d')
        if ed:
            end_date = datetime.strptime(ed, '%Y-%m-%d')
        if sd and ed:
            assert start_date < end_date, Exception(u'日期输入有误')
        page = int(request.args.get('p'))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数传递异常')
    house_query = House.query
    try:
        # 过滤订单时间冲突
        conflict_orders = []
        if start_date and end_date:
            conflict_orders = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date).all()
        elif start_date is not None:
            conflict_orders = Order.query.filter(start_date > Order.begin_date, start_date < Order.end_date).all()
        elif end_date is not None:
            conflict_orders = Order.query.filter(end_date > Order.begin_date, end_date < Order.end_date).all()
        if conflict_orders:
            conflict_house_ids = [order.house_id for order in conflict_orders]  # None不可遍历
            house_query = house_query.filter(House.id.notin_(conflict_house_ids))
        # 筛选地区
        if aid:
            house_query = house_query.filter(House.area_id == aid)
        # 排序
        if sk == 'booking':
            house_query = house_query.order_by(House.order_count.desc())
        elif sk == 'price-inc':
            house_query = house_query.order_by(House.price.asc())
        elif sk == 'price-des':
            house_query = house_query.order_by(House.price.desc())
        else:
            house_query = house_query.order_by(House.create_time.desc())
        # 分页flask-sqlalchemy/__init__:430
        # class BaseQuery  def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
        paginate = house_query.paginate(page, config.HOUSE_LIST_PAGE_CAPACITY, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'房屋查询失败')
    house_list = []
    for house in paginate.items:
        house_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg='OK', data={'houses': house_list, 'total_page': paginate.pages})
