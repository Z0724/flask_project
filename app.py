from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from newproject import app, db, admin
from newproject.models import User
from newproject.forms import LoginForm, RegistrationForm




@app.route('/',methods=['POST','GET'])
def base_test():
    return render_template('base_test.html')

@app.route('/login',methods=['POST','GET'])
def base_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("您已經成功的登入系統")
            next = request.args.get('next')
            if  next == None or not next[0]=='/':
                next = url_for('base_test')
            return redirect(next)
    return render_template('base_login.html',form=form)

@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("您已經登出")
    return redirect(url_for('base_test.html'))

@app.route('/test',methods=['POST','GET'])
def test():
    return render_template('test.html')



@app.route("/base_signup",methods=['POST','GET'])
def base_signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data, password=form.password.data)

        # add to db table
        db.session.add(user)
        db.session.commit()
        flash("註冊成功")
        return redirect(url_for('base_login'))
    return render_template('base_signup.html',form=form)

@app.route('/base_member',methods=['POST','GET'])
@login_required
def welcome_user():
    return render_template('base_member.html')


if __name__ == "__main__":
	app.run()
# app.run(host=”你想要的ip”,port=”你想要的port”,debug=True)