from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, validators, TextAreaField
from flask_login import current_user
from newproject.blog.model import Blog_Main, Blog_Category
from newproject.models import User

class Form_Blog_Main(FlaskForm):
    blog_name = StringField('部落格名稱', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])
    blog_descri = TextAreaField('簡介', validators=[
        validators.Length(0, 300)
    ])
    submit = SubmitField('建立部落格')


class Form_Blog_Post(FlaskForm):
    post_title = StringField('文章標題', validators=[
        validators.DataRequired(),
        validators.Length(1, 80)
    ])
    post_body = TextAreaField('文章內容', validators=[
        validators.DataRequired()
    ])

    post_blog = SelectField('選擇部落格', coerce=int)
    post_category = SelectField('文章分類', coerce=int)
    submit = SubmitField('發文')
    def __init__(self):
        super(Form_Blog_Post, self).__init__()
        self.post_blog.choices = [(a.id, a.blog_name)
                            for a in Blog_Main.query.filter_by(author=current_user.id).all()]
        self.post_category.choices =  [(b.id,  b.name)
                            for b in Blog_Category.query.order_by().all()]
