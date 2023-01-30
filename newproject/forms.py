from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, validators
from wtforms.validators import DataRequired, Email, EqualTo, email_validator
from wtforms import ValidationError
from newproject.models import User
from newproject.main.form import FormUserInfo
# 這邊放表單相關涵式

# 登入
class LoginForm(FlaskForm):
    email = StringField('信箱', validators=[DataRequired(), Email()])
    password = PasswordField('密碼',validators=[DataRequired()])
    remember_me = BooleanField('保持登入')
    submit = SubmitField('登入')

# 註冊
class RegistrationForm(FlaskForm):
    email = StringField('註冊信箱', validators=[DataRequired(), Email()])
    username = StringField('您的暱稱', validators=[DataRequired()])
    password = PasswordField('註冊密碼', validators=[DataRequired(), EqualTo('pass_confirm', message='密碼需要吻合')])
    pass_confirm = PasswordField('確認密碼', validators=[DataRequired()])
    submit = SubmitField('註冊')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('電子郵件已經被註冊過了')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('使用者名稱已經存在')

# 留言板
class messageForm(FlaskForm):
    mb_title = StringField('標題', validators=[DataRequired()])
    mb_username = StringField('暱稱',validators=[DataRequired()])
    mb_message = TextAreaField('內容',validators=[DataRequired()])
    submit = SubmitField('送出')


# 權限註冊
class FormFunc(FlaskForm):
    func_module_name = StringField('權限名稱', validators=[
        validators.DataRequired(),
        validators.Length(max=50, message="Max Length equal 50")
    ])
    func_description = StringField('權限說明', validators=[
        validators.DataRequired(),
        validators.Length(max=100, message="Max Length equal 100")
    ])
    func_is_activate = BooleanField('是否啟用', default="checked")
    func_remark = StringField('備註', validators=[
        validators.DataRequired(),
        validators.Length(max=100, message="Max Length equal 100")
    ])
    submit = SubmitField('增加新權限')

# Role角色管理用表單
class FormRole(FlaskForm):
    name = StringField('角色名稱', validators=[
        validators.DataRequired(),
        validators.Length(max=50, message='Max Length equal 50')
    ])

    submit = SubmitField('增加新角色')