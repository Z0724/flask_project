from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField, TextAreaField

class FormUserInfo(FlaskForm):
    # 使用者資料編修
    about_me = TextAreaField('關於我', validators=[
        validators.DataRequired()
    ])
    location = StringField('國家', validators=[
        validators.DataRequired(),
        validators.Length(1, 20)
    ])
    #  使用下拉選單來選擇性別
    gender = SelectField('性別', validators=[
        validators.DataRequired()
     ], choices=[('F', '女'), ('M', '男')])
    submit = SubmitField('送出')