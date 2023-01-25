from flask import Blueprint
#  定義
blog = Blueprint('blog', __name__)
#  關聯
from . import view