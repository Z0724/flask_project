import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']= 'ffsdfsddsbr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#指定ADMIN樣式
app.config['FLASK_ADMIN_SWATCH']='cerulean'
#初始化ADMIN
admin = Admin(app, name='就是後台', template_mode='bootstrap3')



db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

