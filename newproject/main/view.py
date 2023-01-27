from flask_login import login_required, current_user
from flask import render_template, url_for, flash, redirect, abort
from . import main, errorhandler
from newproject.forms import FormUserInfo, FormFunc
from newproject import db
from newproject.models import User, Func


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