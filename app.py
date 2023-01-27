from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from newproject import app, db, admin
from newproject.models import User, message_board, Role, Func
from newproject.blog.model import Blog_Category, Blog_Main, Blog_Post
from newproject.forms import LoginForm, RegistrationForm, messageForm
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_paginate import Pagination, get_page_parameter

@app.route('/test',methods=['POST','GET'])
def test():
    return render_template('test.html')

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('base_test.html')

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            # 第二個參數是記得我的參數
            login_user(user, form.remember_me.data)
            flash("您已經成功的登入系統")
            # 利用request來取得參數next，上個頁面在哪
            next = request.args.get('next')
            # 自定義一個驗證的function來確認使用者是否確實有該url的權限
            # 另一個用法if not next_is_valid(next):
            # next_is_valid需要另外寫函式next_is_valid(url):return True
            if  next == None or not next[0]=='/':
                next = url_for('index')
            return redirect(next)
        else:
            #  如果資料庫無此帳號或密碼錯誤，就顯示錯誤訊息。
            flash('信箱或密碼錯誤')
    return render_template('base_login.html',form=form)

@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("您已經登出")
    return redirect(url_for('test'))

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
        return redirect(url_for('login'))
    return render_template('base_signup.html',form=form)

@app.route('/member',methods=['POST','GET'])
@login_required
#需要登入才能進入
def welcome_user():
    return render_template('base_member.html')

@app.route('/myself',methods=['POST','GET'])
def base_myself():
    return render_template('base_myself.html')

@app.route('/message',methods=['POST','GET'])
@app.route('/message/<int:page>/',methods=['POST','GET'])
def mb_message(page=1):
    form = messageForm()
    if form.validate_on_submit():
        message = message_board(mb_title=form.mb_title.data,
        mb_username=form.mb_username.data, mb_message=form.mb_message.data)

        # add to db table
        db.session.add(message)
        db.session.commit()
        flash("留言成功")
        return redirect(url_for('mb_message', posts=posts))
    
    # page = message_board.query.paginate(page=1, per_page=3).all()
    # posts = db.paginate(db.select(message_board).order_by(message_board.mb_id, message_board.mb_title, message_board.mb_username, message_board.mb_message, message_board.mb_data),per_page=3)
    # page = request.args.get(get_page_parameter(), type=int, default=int(page))
    # err = message_board.query.filter_by().first_or_404()
    # pagination = Pagination(page=page, total=12,per_page=5)
    # posts = message_board.query.paginate(page=1, per_page=3).items()
    posts=message_board.query.filter_by().paginate(page=page,per_page=3)


    return render_template('base_message.html',form=form,posts=posts)
    # , views=message_board.query.all()

    

#後台
class backindex(BaseView):
    @expose('/')
    def index(self):
        return render_template('base_test.html')
class MyView2(BaseView):
    @expose('/')
    def index(self):
        return self.render('base_admin2.html')

admin.add_view(backindex(name='回主頁'))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(message_board, db.session))
admin.add_view(ModelView(Blog_Category, db.session))
admin.add_view(ModelView(Blog_Main, db.session))
admin.add_view(ModelView(Blog_Post, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Func, db.session))
admin.add_view(MyView2(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView2(name='Hello 2', endpoint='test2', category='Test'))

if __name__ == "__main__":
	app.run()
# app.run(host=”你想要的ip”,port=”你想要的port”,debug=True)