from newproject import app, db, login_manager, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from sqlalchemy import text

##  設置中繼的關聯表
#  flask-sqlalchemy會自動的在資料庫中產生相對應的table
relations_user_role = db.Table('relation_user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))
relations_role_func = db.Table('relations_role_func',
    db.Column('func_id', db.Integer, db.ForeignKey('funcs.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


# 這邊放資料庫相關涵式

# 權限角色主表
class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    #  利用secondary設置關聯中繼表
    #  lazy的部份可以依需求設置為動態與否
    funcs = db.relationship('Func', secondary=relations_role_func, lazy='subquery',
                            backref=db.backref('roles', lazy=True))
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Role is %s' % self.name


class Func(db.Model):
    __tablename__ = 'funcs'
    id = db.Column(db.Integer, primary_key=True)
    func_module_name = db.Column(db.String(50))
    func_description = db.Column(db.String(100))
    func_is_activate = db.Column(db.Boolean, default=True)
    func_remark = db.Column(db.String(100))

    def __init__(self, func_module_name, func_description, func_is_activate=True, func_remark=None):
        self.func_module_name = func_module_name
        self.func_description = func_description
        self.func_is_activate = func_is_activate
        self.func_remark = func_remark

    def __repr__(self):
        return 'id = %i, module_name = %s, is_activate = %s'
    

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
    blog_mains = db.relationship('Blog_Main', backref='user', lazy='dynamic')
    blog_posts = db.relationship('Blog_Post', backref='user', lazy='dynamic')
    #  利用secondary設置關聯中繼表
    #  lazy的部份可以依需求設置為動態與否
    roles = db.relationship('Role', secondary=relations_user_role, lazy='subquery',
                               backref=db.backref('users', lazy=True))
    def __init__(self, email, username, password):
        # """初始化"""
        self.email = email
        self.username = username
        # 實際存入的為password_hash，而非password本身
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # """檢查使用者密碼"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def user_func(self):
        func_list = Func.query.join(relations_role_func) \
                        .join(Role) \
                        .join(relations_user_role) \
                        .join(User) \
                        .filter(User.id == self.id)
        return func_list
    
    # 檢查使用者是否有權限進入該View Function
    def check_author(self, func_module, func_name):
        #  取得個人的權限表
        func_list = self.user_func
        #  func的table中記錄是module+.+func_name
        view_function = func_module + '.' + func_name
        result = func_list.filter(text("func_module_name=:view_function")) \
            .params(view_function=view_function).first()
        if result:
            return True
        else:
            return False   
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
        self.mb_title = mb_title
        self.mb_username = mb_username
        self.mb_message = mb_message





with app.app_context():
    db.create_all()

# 可以依照user_id，對應出資料庫中實際的User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


