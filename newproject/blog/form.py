from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, validators, TextAreaField
from flask_login import current_user
from newproject.blog.model import Blog_Main, Blog_Category

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

    post_blog = SelectField('選擇部落格')
    post_category = SelectField('文章分類', coerce=str)
    submit = SubmitField('發文')
    def __init__(self):
        super(Form_Blog_Post, self).__init__()
        self.post_blog.choices = self._get_blog_main()
        self.post_category.choices = self._get_category()

    def _get_blog_main(self):
        obj = Blog_Main.query.with_entities(Blog_Main.blog_name).filter_by(author=current_user._get_current_object().id).all()
        return obj
    def _get_category(self):
        obj = Blog_Category.query.with_entities(Blog_Category.name).all()
        return obj

