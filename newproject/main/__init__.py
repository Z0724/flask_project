from flask import Blueprint

#  定義
main = Blueprint('main', __name__, template_folder='templates')
# , static_folder='static'
#  關聯
from . import view, errorhandler