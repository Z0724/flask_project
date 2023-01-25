from newproject import db, app
from datetime import datetime
from newproject.models import User

class Blog_Main(db.Model):
    __tablename__ = 'BlogMains'
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(30), nullable=False)
    blog_descri = db.Column(db.String(200))
    blog_create_date = db.Column(db.DateTime, default=datetime.utcnow)
    #  設置fk關聯使用者id
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    posts = db.relationship('Blog_Post', backref='blogs', lazy='dynamic')

    def __init__(self, blog_name, blog_descri, author):
        self.blog_name = blog_name
        self.blog_descri = blog_descri
        self.author = author

    def __repr__(self):
        return '<blog>:%s, <author>:%s' % (self.blog_name, self.author)

# 文章類別
class Blog_Category(db.Model):
    __tablename__ = 'Blog_Categorys'
    id = db.Column(db.Integer, primary_key=True)
    # 類別名稱
    name = db.Column(db.String(50))
    # remark = db.Column(db.Integer, db.ForeignKey('Blog_Posts'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category> %s' % self.name

class Blog_Post(db.Model):
    __tablename__ = 'Blog_Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    # 文章內容
    body = db.Column(db.Text)
    # 文章類別(可以依需求設置為多對多)
    category_id = db.Column(db.Integer, db.ForeignKey(Blog_Category.id))
    # 作者
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # blog
    blog_main_id = db.Column(db.Integer, db.ForeignKey(Blog_Main.id))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 網址
    slug = db.Column(db.String(256), unique=True)
    # 是否存活
    flag = db.Column(db.Boolean, default=True)
    categorys = db.relationship('Blog_Category', backref=db.backref('posts', lazy='dynamic'))


    def __init__(self, title, body, category, author, blog_main, slug=None):
        self.title = title
        self.body = body
        self.category_id = category
        self.author_id = author.id
        self.blog_main_id = blog_main
        self.slug = slug

    def __repr__(self):
        return '<POST> %s' % self.title















with app.app_context():
    db.create_all()