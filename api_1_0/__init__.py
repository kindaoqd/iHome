# -*- coding: utf-8 -*-
from flask import Blueprint
api = Blueprint('api', __name__, url_prefix='/api/1.0')  # 一个蓝图对象可记录多个视图，无需建立多个

from . import index, verify, passport, profile, house
