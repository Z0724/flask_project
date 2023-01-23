import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy, query
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_babelex import Babel #中文化後台
from flask_bootstrap import Bootstrap

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']= 'ffsdfsddsbr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 中文化後台
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# 快速套版用
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
# 遷移資料表或調整欄位用
Migrate(app,db)
# 設置flask-login中對session的安全等級
SESSION_PROTECTION = 'strong'
# 初始化flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 初始化ADMIN
admin = Admin(app, name='就是後台', template_mode='bootstrap3')
# 定義Blueprint
# author = Blueprint('author', __name__)

