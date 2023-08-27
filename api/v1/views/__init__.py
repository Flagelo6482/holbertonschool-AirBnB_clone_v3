"""First blueprint"""
from flask import Blueprint

"""New instance Blueprint"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""wildcard import of everything in the package"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *