from newproject import db, login_manager, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from newproject import app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt


# 這邊放資料庫相關涵式


# UserMixin記錄用戶狀態
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    # columns
    id       = db.Column(db.Integer, primary_key = True)
    email    = db.Column(db.String(64),unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    location = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    regist_date = db.Column(db.DateTime, default = datetime.utcnow())
    last_login = db.Column(db.DateTime, default = datetime.utcnow())
    blog_mains = db.relationship('Blog_Main', backref='user', lazy='dynamic'
)
    blog_posts = db.relationship('Blog_Post', backref='user', lazy='dynamic')
    def __init__(self, email, username, password):
        # """初始化"""
        self.email = email
        self.username = username
        # 實際存入的為password_hash，而非password本身
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # """檢查使用者密碼"""
        return check_password_hash(self.password_hash, password)
# bcrypt 加密密碼

class message_board(db.Model):
    __tablename__ = 'message_board'
    
    # columns
    mb_id       = db.Column(db.Integer, primary_key = True)
    mb_title    = db.Column(db.String(64), unique=True, index=True)
    mb_username = db.Column(db.String(64), index=True)
    mb_message = db.Column(db.String(300))
    mb_data = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self, mb_title, mb_username, mb_message):
        """初始化"""
        self.mb_title = mb_title
        self.mb_username = mb_username
        self.mb_message = mb_message

with app.app_context():
    db.create_all()

# 可以依照user_id，對應出資料庫中實際的User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


