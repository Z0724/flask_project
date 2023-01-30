from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField, TextAreaField
from wtforms import SelectMultipleField, widgets
from newproject.models import Func, Role, User

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
    all_function_option = MultiCheckboxField('權限勾選', coerce=int)
    submit = SubmitField('送出')

# 使用者角色管理界面
class Form_User_Role_manager(FlaskForm):
    all_role_option = MultiCheckboxField('角色勾選', coerce=int)
    submit = SubmitField('送出')

# 選擇要修改的權限
class Form_Func_edit(FlaskForm):
    Func_edit = SelectField('選擇要修改的權限', coerce=int)
    submit = SubmitField('送出')
    def __init__(self):
        super(Form_Func_edit, self).__init__()
        self.Func_edit.choices = [(a.id, a.func_module_name)
                            for a in Func.query.order_by().all()]
                            
# 選擇要修改的角色
class Form_Role_edit(FlaskForm):
    Role_edit = SelectField('選擇要修改哪個角色的名稱', coerce=int)
    submit = SubmitField('送出')
    def __init__(self):
        super(Form_Role_edit, self).__init__()
        self.Role_edit.choices = [(a.id, a.name)
                            for a in Role.query.order_by().all()]

# 選擇要修改的角色
class Form_Role_Func_edit(FlaskForm):
    Role_Func_edit = SelectField('選擇要修改哪個角色的權限', coerce=int)
    submit = SubmitField('送出')
    def __init__(self):
        super(Form_Role_Func_edit, self).__init__()
        self.Role_Func_edit.choices = [(a.id, a.name)
                            for a in Role.query.order_by().all()]

# 選擇要修改的使用者角色
class Form_User_Role_edit(FlaskForm):
    User_Role_edit = SelectField('選擇要修改哪個使用者的角色', coerce=int)
    submit = SubmitField('送出')
    def __init__(self):
        super(Form_User_Role_edit, self).__init__()
        self.User_Role_edit.choices = [(a.id, a.username)
                            for a in User.query.order_by().all()]