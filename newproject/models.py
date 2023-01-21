from newproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from newproject import app
from flask_sqlalchemy import SQLAlchemy


# 這邊放資料庫相關涵式


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    # columns
    id       = db.Column(db.Integer, primary_key = True)
    email    = db.Column(db.String(64),unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))
    def __init__(self, email, username, password):
        """初始化"""
        self.email = email
        self.username = username
        # 實際存入的為password_hash，而非password本身
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """檢查使用者密碼"""
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()

# 可以依照user_id，對應出資料庫中實際的User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


