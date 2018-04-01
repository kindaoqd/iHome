# -*- coding: utf-8 -*-
from flask import Blueprint
url_prefix = '/api/1.0'
api = Blueprint('api', __name__, url_prefix=url_prefix)
verify_blue = Blueprint('verify_blue', __name__,  url_prefix=url_prefix)

from . import index, verify
