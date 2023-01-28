from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField, TextAreaField
from wtforms import SelectMultipleField, widgets

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

#  建立MultiCheckboxField
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
# 角色權限管理界面
class FormRole_Func_manager(FlaskForm):
    all_function_option = MultiCheckboxField('all_function', coerce=int)
    submit = SubmitField('submit')

# 使用者角色管理界面
class Form_User_Role_manager(FlaskForm):
    all_role_option = MultiCheckboxField('all_role', coerce=int)
    submit = SubmitField('submit')