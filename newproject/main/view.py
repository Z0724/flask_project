from flask_login import login_required, current_user
from flask import render_template, url_for, flash, redirect, abort
from . import main, errorhandler
from newproject.forms import FormUserInfo, FormFunc, FormRole
from newproject import db
from newproject.models import User, Func, Role
from newproject.main.form import FormRole_Func_manager, Form_User_Role_manager


@main.route('/edituserinfo', methods=['GET', 'POST'])
@login_required
def edituserinfo():
    form = FormUserInfo()
    if form.validate_on_submit():
        # current_user等於現在登入的使用者
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        current_user.gender = form.gender.data
        # add to db table
        db.session.add(current_user)
        db.session.commit()
        flash("修改成功")
        return redirect(url_for('main.userinfo', username=current_user.username))
    #  預設表單欄位資料為user的目前值
    form.about_me.data = current_user.about_me
    form.location.data = current_user.location
    form.gender.data = current_user.gender
    return render_template('main/editUserInfo.html', form=form)

@main.route('/userinfo/<username>')
def userinfo(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/UserInfo.html', user=user)

# 註冊View_Function
@main.route('/viewfunction/c/', methods=['GET', 'POST'])
def view_function_c():
    form = FormFunc()
    if form.validate_on_submit():
        func = Func(
            func_module_name=form.func_module_name.data,
            func_description=form.func_description.data,
            func_is_activate=form.func_is_activate.data,
            func_remark=form.func_remark.data)
        db.session.add(func)
        db.session.commit()
        flash('New Func %s Register Success..' % form.func_module_name.data)
        return redirect(url_for('main.view_function_c'))
    return render_template('main/createViewFunction.html', form=form)

# 查詢View Function List
@main.route('/viewfunction/r', methods=['GET'])
@main.route('/viewfunction/r/<int:page>/', methods=['GET'])
def view_function_r(page=1):
    #  欄位名稱
    columns = ['ID', 'Module_Name', 'Func_Description', 'is_activate' , 'Func_Remark']
    funcs = Func.query.filter_by().paginate(page=page,per_page=5)
    return render_template('main/readViewFunction.html', funcs=funcs, columns=columns)

# 編輯View Function,利用WTForm的obj來渲染Model讀出的資料，前提在於兩邊的名稱設置需要一致。
@main.route('/viewfunction/e/<int:func_id>/', methods=['GET', 'POST'])
@login_required
def view_function_e(func_id):
    func = Func.query.filter_by(id=func_id).first_or_404()
    form = FormFunc(obj=func)
    if form.validate_on_submit():
        form.populate_obj(func)
        db.session.commit()
        flash('更新成功!')
        return redirect(url_for('main.view_function_r', page=1))
    return render_template('main/createViewFunction.html', form=form)

# 建立角色
@main.route('/rolemanager/c/', methods=['GET', 'POST'])
@login_required
def role_manager_c():
    form = FormRole()
    if form.validate_on_submit():
        role = Role(
            name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('New Role %s Register Success..' % form.name.data)
        return redirect(url_for('main.role_manager_c'))
    return render_template('main/managerRole.html', form=form, action='create')


# 查詢Role
@main.route('/rolemanager/r', methods=['GET'])
@main.route('/rolemanager/r/<int:page>/', methods=['GET'])
@login_required
def role_manager_r(page=1):
    #  欄位名稱
    columns = ['ID', 'Role_Name']
    roles = Role.query.filter_by().paginate(page=page,per_page=5)
    return render_template('main/readRole.html', roles=roles, columns=columns)

# 編輯Role
# 利用WTForm的obj來渲染Model讀出的資料，前提在於兩邊的名稱設置需要一致。
@main.route('/rolemanager/e/<int:role_id>/', methods=['GET', 'POST'])
@login_required
def role_manager_e(role_id):
    role = Role.query.filter_by(id=role_id).first_or_404()
    form = FormRole(obj=role)
    if form.validate_on_submit():
        form.populate_obj(role)
        db.session.commit()
        flash('Update Role Success!')
        return redirect(url_for('main.role_manager_r', page=1))
    return render_template('main/managerRole.html', form=form, action='edit')


# 角色權限管理
# 取得角色目標權限以及未存在的權限
@main.route('/role_func_manager/<int:role_id>/', methods=['GET', 'POST'])
def role_func_manager(role_id):
    form = FormRole_Func_manager()
    #  取得角色
    role = Role.query.filter_by(id=role_id).first()
    #  取得目前擁有的View function list
    all_funcs = Func.query.with_entities(Func.id, Func.func_module_name).all()
    #  設置checkbox的項目
    form.all_function_option.choices = [(id, role) for id, role in all_funcs]
    #  以該角色目前擁有的權限做為預設值
    form.all_function_option.default = [role.id for role in role.funcs]
    if form.validate_on_submit():
        #  取得選取得View function項目
        funcs = Func.query.filter(Func.id.in_(form.all_function_option.data))
        #  先清空
        role.funcs.clear()
        for func in funcs:
            #  後寫入
            role.funcs.append(func)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('main.role_manager_r', page=1))
    #  務必執行，預設值才會成功
    form.process()
    return render_template('main/Role_Func_manager.html', form=form)

# 使用者角色管理
@main.route('/user_role_manager/<int:user_id>/', methods=['GET', 'POST'])
def user_role_manager(user_id):
    form = Form_User_Role_manager()
    #  取得使用者資料
    user = User.query.filter_by(id=user_id).first()
    #  取得目前擁有的Role list
    all_roles = Role.query.with_entities(Role.id, Role.name).all()
    #  設置checkbox的項目
    form.all_role_option.choices = [(id, name) for id, name in all_roles]
    #  以使用者目前擁有的角色為預設值
    form.all_role_option.default = [role.id for role in user.roles]
    if form.validate_on_submit():
        #  取得選取得Role項目
        roles = Role.query.filter(Role.id.in_(form.all_role_option.data))
        #  先清空
        user.roles.clear()
        for role in roles:
            #  後寫入
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash('Modify %s Role Success!' % user.username)
        return redirect(url_for('index'))
    #  務必執行，預設值才會成功
    form.process()
    return render_template('main/User_Role_manager.html', form=form)